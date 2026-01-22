from graphnet.deployment.i3modules import (
        GraphNeTI3Deployer,
        I3InferenceModule,
    )

from graphnet.data.extractors.icecube import (
    I3FeatureExtractorIceCube86,
)
from graphnet.utilities.argparse import ArgumentParser
import yaml
from typing import List
import torch

def main(
    pulsemap: str,
    model_config: str,
    state_dict: str,
    gcd_file: str,
    input_files: List[str],
    output_folder: str,
    model_name:str,
    n_workers:int
) -> None:
        
    """GraphNeTI3Deployer"""
    with open(model_config, "r", encoding="utf-8") as fh: # Open the model configuration YAML file for reading.
        features = yaml.safe_load(fh)['arguments']['graph_definition']["ModelConfig"]["arguments"] #       ["input_feature_names"]
        if features is None:
            features = yaml.safe_load(fh)['arguments']['data_representation']["ModelConfig"]["arguments"]["input_feature_names"]# returns dict/ list/ scalars only
        assert features is not None, "Could not find features in the model config"
    
    if state_dict.endswith('.ckpt'): # Check if the state_dict file is a PyTorch Lightning checkpoint.
        state_dict = torch.load(state_dict, map_location='cpu')['state_dict']

    # Configure Deployment module
    deployment_module = I3InferenceModule( # Create an inference module for deployment on I3 files.
        pulsemap=pulsemap, #blobs amma: liste pos, zeit: charge
        features=features, #namen der features die im model_config.yml definiert sind
        pulsemap_extractor=I3FeatureExtractorIceCube86(pulsemap=pulsemap), #86 kabel ice cube
        model_config=model_config,
        state_dict=state_dict,
        gcd_file=gcd_file, #geometry calibration detector. DOM positions etc
        prediction_columns=["target_pred"], #namen der spalten in denen die vorhersagen gespeichert werden
        model_name = model_name, # name of the model to make prediction
    )

    # Construct I3 deployer
    deployer = GraphNeTI3Deployer( # Create a deployer instance to handle the deployment process.
        graphnet_modules=[deployment_module], # List of GraphNeT modules to be used in deployment.
        n_workers=n_workers, # Number of parallel workers for processing.
        gcd_file=gcd_file, # Path to the GCD file (Geometry, Calibration, DetectorStatus
    )

    # Start deployment - files will be written to output_folder
    deployer.run(
        input_files=input_files,
        output_folder=output_folder,
    )

if __name__ == "__main__":

    # Parse command-line arguments
    parser = ArgumentParser( # ArgumentParser is a utility to handle command-line arguments.
        description="""Getting Prediction directly on I3 files without converting them using GraphNeTI3Deployer."""
    )
   
    parser.add_argument(
        '--pulsemap', 
        type=str, 
        help='Pulsemap used in Training', 
        default='SRTInIcePulses'
    )
    
    parser.add_argument(
        '--model-config', 
        type=str, 
        help='Path to Model Config file (model_config.yml)',
        required=True,
    )
 
    parser.add_argument(
        '--state-dict', #weights
        type=str, 
        help='Path to Model State Dict pytorch file (.pth) or pytorch lightning checkpoint (.ckpt)',
        required=True,
    )
    
    parser.add_argument(
        '--gcd', #geschickt
        type=str, 
        help='Path to GCD file',
        required=True,
    )
    
    parser.add_argument(
        '--input-file-path', #daten file um das es geht. pfad
        nargs='+',
        type=str,
        help='Path to text file with input files listed',
        required=True,
    )
    
    parser.add_argument(
        '--output-folder',  #irgend n folder wo die ergebnisse gespeichert werden
        type=str, 
        help='Path to folder in which I3 files including prediction frame are stored',
        required=True,
    )
    
    parser.add_argument(
        '--model-name', # energy_reco, in liste. in output folder i3 file, in p gruen 
        type=str, 
        help='name of your model to make prediction'
    )

    parser.add_argument(
        "--num-workers", # Number of parallel workers for processing.
        help = "The number of processes to use",
        default=1,
        type=int,
    )
   
    args = parser.parse_args()

    main(
        args.pulsemap,
        args.model_config,
        args.state_dict,
        args.gcd,
        args.input_file_path,
        args.output_folder,
        args.model_name,
        args.num_workers
    )