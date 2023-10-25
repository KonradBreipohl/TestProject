"""Functionalities for managing and calling configurators."""
from up_ac.AC_interface import *
from up_ac.configurators import Configurator

import timeit
import os
import sys
from threading import Thread
from queue import Queue
import subprocess
import dill 
import shutil
from unified_planning.exceptions import UPProblemDefinitionError
from pebble import concurrent
from concurrent.futures import TimeoutError


class OATConfigurator(Configurator):
    """Configurator functions."""

    def __init__(self):
        """Initialize OAT configurator."""
        Configurator.__init__(self)

    def get_OAT_incumbent(self):

        path = self.scenario['path_to_OAT']
        read_param = False
        config = {}
        with open(f'{path}tunerLog.txt', 'r') as f:
            for line in f:
                line = line.split(' ')
                for i, l in enumerate(line):
                    line[i] = l.replace(' ', '')
                if 'results' in line:
                    read_param = False
                if read_param:
                    param_name = str(line[0].replace('\t', '')[:-1])
                    config[param_name] = line[1].replace('\n', '')      
                if 'according' in line:
                    read_param = True
                    
        return config

    def get_feedback_function(self, gaci, engine, metric, mode,
                              gray_box=False):
        """
        Generate the function to run the engine and obtain feedback.

        :param gaci: AC interface object.
        :param str engine: Engine name.
        :param str metric: Optimization metric ('runtime' or 'quality').
        :param str mode: Type of planning.
        :param bool gray_box: True if gray box to use.

        :return: Planner feedback function.
        :rtype: function
        """

        if engine in self.capabilities[metric][mode]:
            self.metric = metric

            if gray_box:
                class gb_out():
                    def __init__(self, q, res):
                        self.q = q
                        self.res = res

                    def write(self, txt):
                        # TODO
                        # pass output to configurator
                        if self.res.empty():
                            self.q.put(txt)
                q = Queue()
                res = Queue()
                gb_out = gb_out(q, res)

            def planner_feedback(config, instance, reader):
                """
                Planner feedback function.

                :param config: Configuration for the planner.
                :param instance: Problem instance.
                :param reader: Reader object for parsing the problem.

                :return: Feedback value based on the planner's performance.
                :rtype: float
                """

                path = os.getcwd().rsplit('up-ac', 1)[0]
                path += 'up-ac/up_ac'
                sys.path.append(r"{}".format(path))

                self.reader = reader 
                
                start = timeit.default_timer()
                instance_p = f'{instance}'
                domain_path = instance_p.rsplit('/', 1)[0]
                domain = f'{domain_path}/domain.pddl'
                pddl_problem = self.reader.parse_problem(f'{domain}',
                                                         f'{instance_p}')
                # gray box in OAT only works with runtime scenarios
                if gray_box:
                    def planner_thread(gb_out, problem, res,
                                       config, metric, engine, mode, 
                                       pddl_problem):
                        res.put(
                            gaci.run_engine_config(config,
                                                   metric,
                                                   engine,
                                                   mode,
                                                   pddl_problem,
                                                   gb_out))

                    thread = Thread(target=planner_thread,
                                    args=(gb_out, pddl_problem, res,
                                          config, metric, engine, mode, 
                                          pddl_problem),
                                    daemon=True)

                    thread.start()

                    while thread.is_alive():
                        try:
                            output = q.get(False)
                        except:
                            output = None
                        if output is not None and len(output) not in (0, 1):
                            print('gray box:', output)
                        if not res.empty():
                            thread.join()

                    feedback = res.get()

                else:
                    feedback = \
                        gaci.run_engine_config(config,
                                               metric,
                                               engine,
                                               mode,
                                               pddl_problem)
                                               
                    try:
                        @concurrent.process(timeout=self.scenario['timelimit'])
                        def solve(config, metric, engine,
                                  mode, pddl_problem):
                            feedback = \
                                gaci.run_engine_config(config,
                                                       metric, engine,
                                                       mode, pddl_problem)

                            return feedback

                        feedback = solve(config, metric, engine,
                                         mode, pddl_problem)
                    
                        try:
                            feedback = feedback.result()
                        except TimeoutError:
                            if metric == 'runtime':
                                feedback = self.planner_timelimit
                            elif metric == 'quality':
                                feedback = self.crash_cost

                    except (AssertionError, NotImplementedError,
                            UPProblemDefinitionError):
                        print('\n** Error in planning engine!')
                        if metric == 'runtime':
                            feedback = self.planner_timelimit
                        elif metric == 'quality':
                            feedback = self.crash_cost

                if feedback is not None:
                    if metric == 'quality':
                        self.print_feedback(engine, instance_p, feedback)
                        return -feedback
                    elif metric == 'runtime':
                        if engine in ('tamer', 'pyperplan'):
                            feedback = timeit.default_timer() - start
                            self.print_feedback(engine, instance_p, feedback)
                        else:
                            feedback = feedback
                            self.print_feedback(engine, instance_p, feedback)
                        return feedback
                else:
                    # Penalizing failed runs
                    if metric == 'runtime':
                        # Penalty is max runtime in runtime scenario
                        feedback = self.scenario['timelimit']
                        self.print_feedback(engine, instance_p, feedback)
                    else:
                        # Penalty is defined by user in quality scenario
                        feedback = self.crash_cost
                        self.print_feedback(engine, instance_p, feedback)

                    return feedback

            path_to_OAT = 'path_to_OAT'

            dill.dump(
                planner_feedback, open(
                    f'{self.scenario[path_to_OAT]}feedback.pkl', 'wb'),
                recurse=True)

            planner_feedback = f'{self.scenario[path_to_OAT]}call_engine_OAT.py'

            return planner_feedback
        else:
            print(f'Algorithm Configuration for {metric} of {engine} in' + \
                  ' {mode} is not supported.')
            return None

    def set_scenario(self, engine, param_space, gaci,
                     configuration_time=120, n_trials=400, min_budget=1,
                     max_budget=3, crash_cost=0, planner_timelimit=30,
                     n_workers=1, instances=[], instance_features=None,
                     metric='runtime', popSize=128, evalLimit=2147483647):
        """
        Set up algorithm configuration scenario.

        :param str engine: Engine name.
        :param param_space: ConfigSpace object.
        :param gaci: AC interface object.
        :param int configuration_time: Overall configuration time budget.
        :param int n_trials: Maximum number of engine evaluations.
        :param int min_budget: Minimum number of instances to use.
        :param int max_budget: Maximum number of instances to use.
        :param int crash_cost: Cost to use if engine fails.
        :param int planner_timelimit: Maximum runtime per evaluation.
        :param int n_workers: Number of cores to utilize.
        :param list instances: Problem instance paths.
        :param instance_features: Dictionary of instance names and lists of features.
        :param str metric: Optimization metric.
        :param int popSize: Population size of configs per generation (OAT).
        :param int evalLimit: Maximum number of evaluations (OAT).
        """

        if not instances:
            instances = self.train_set
        self.crash_cost = crash_cost

        param_file = gaci.get_ps_oat(param_space)

        path = os.getcwd().rsplit('up-ac', 2)[0]
        path += 'up-ac/up_ac'

        path_to_xml = f'{path}/OAT/{engine}parameterTree.xml'

        oat_dir = f'{path}/OAT/'

        with open(path_to_xml, 'w') as xml:
            xml.write(param_file)

        inst_dir = f'{path}/OAT/{engine}'

        if os.path.isdir(inst_dir):
            shutil.rmtree(inst_dir, ignore_errors=True)

        os.mkdir(inst_dir)
        file_name = 0
        for inst in instances:
            with open(f'{inst_dir}/{file_name}.txt', 'w') as f:
                f.write(f'{inst}')
            file_name += 1

        scenario = dict(
            xml=path_to_xml,
            timelimit=planner_timelimit,
            wallclock=configuration_time,
            start_gen=min_budget,
            end_gen=max_budget,
            n_workers=n_workers,
            metric=metric,
            instance_dir=inst_dir,
            path_to_OAT=oat_dir,
            popSize=popSize,
            evalLimit=evalLimit
        )

        self.scenario = scenario

    def optimize(self, feedback_function=None, gray_box=False):
        """
        Run the algorithm configuration.

        :param function feedback_function: Function to run the engine and get feedback.
        :param bool gray_box: True if gray box usage.

        :return: Tuple containing the best configuration found and None.
        :rtype: tuple
        """

        if feedback_function is not None:

            print('\nStarting Parameter optimization\n')

            if self.scenario['metric'] == 'quality':
                tunefor = ' --byValue '
            elif self.scenario['metric'] == 'runtime':
                tunefor = ' --enableRacing=true '
            
            n_workers = self.scenario['n_workers']
            path_to_OAT = self.scenario['path_to_OAT']
            param_space = self.scenario['xml']
            instance_folder = self.scenario['instance_dir']
            planner_timelimit = self.scenario['timelimit']
            min_budget = self.scenario['start_gen']
            max_budget = self.scenario['end_gen']
            evalLimit = self.scenario['evalLimit']
            popSize = self.scenario['popSize']

            p = subprocess.Popen(['./Optano.Algorithm.Tuner.Application' +
                                  ' --master' +
                                  f' --maxParallelEvaluations={n_workers} ' + 
                                  '--basicCommand=\"python3 ' + 
                                  f'{feedback_function} {{instance}} ' + 
                                  '{{arguments}}\"' + 
                                  f' --parameterTree={param_space} ' + 
                                  '--trainingInstanceFolder' +
                                  f'=\"{instance_folder}\" ' + 
                                  f'--cpuTimeout={planner_timelimit}' + 
                                  f'{tunefor}' + 
                                  f'--numGens={max_budget} ' + 
                                  f'--goalGen={min_budget} ' +
                                  f'--instanceNumbers={min_budget}:' +
                                  f'{max_budget} ' +
                                  f'--evaluationLimit={evalLimit} ' +
                                  f'--popSize={popSize}'],
                                 stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                 cwd=f'{path_to_OAT[:-1]}', shell=True)

            while p.poll() is None:
                line = p.stdout.readline()
                print(line.decode('utf-8'))

            self.incumbent = self.get_OAT_incumbent()

            print('\nBest Configuration found is:\n',
                  self.incumbent)

            return self.incumbent, None
        else:
            return None, None
