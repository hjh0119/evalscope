from collections import defaultdict
from typing import Any, Dict, List

from evalscope.benchmarks import Benchmark, DataAdapter
from evalscope.constants import EvalType
from evalscope.metrics import Metric, mean, metric_registry


@Benchmark.register(
    name='ifeval',
    pretty_name='IFEval',
    tags=['Instruction-Following'],
    description=
    'IFEval is a benchmark for evaluating instruction-following language models, focusing on their ability to understand and respond to various prompts. It includes a diverse set of tasks and metrics to assess model performance comprehensively.',  # noqa: E501
    dataset_id='opencompass/ifeval',
    subset_list=['default'],
    metric_list=[
        'prompt_level_strict_acc',
        'inst_level_strict_acc',
        'prompt_level_loose_acc',
        'inst_level_loose_acc',
    ],
    few_shot_num=0,
    train_split=None,
    eval_split='train',
    prompt_template='',
)
class IFEvalAdapter(DataAdapter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # register metrics
        metric_registry.register(Metric(name='prompt_level_strict_acc', object=mean))
        metric_registry.register(Metric(name='inst_level_strict_acc', object=mean))
        metric_registry.register(Metric(name='prompt_level_loose_acc', object=mean))
        metric_registry.register(Metric(name='inst_level_loose_acc', object=mean))

    def gen_prompt(self, input_d: dict, subset_name: str, few_shot_list: list, **kwargs) -> Any:
        return self.gen_prompt_data(input_d['prompt'])

    def get_gold_answer(self, input_d: dict) -> str:
        return input_d

    def match(self, gold: Any, pred: Any) -> Dict:
        from evalscope.benchmarks.ifeval.utils import process_results

        return process_results(gold, [pred])

    def compute_metric(self, review_res_list: List[dict], **kwargs) -> Any:
        # aggregate review results
        res_dict = super().compute_dict_metric(review_res_list, **kwargs)

        return super().compute_metric(res_dict, **kwargs)
