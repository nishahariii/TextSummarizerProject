from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.data_transformation import DataTransformation
from textSummarizer.logging import logger

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        # data_transformation_config = DataTransformationConfig(
        #     root_dir=data_transformation_config.root_dir,
        #     data_path=data_transformation_config.data_path,
        #     tokenizer_name="google/pegasus-cnn_dailymail"
        # )
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.convert()