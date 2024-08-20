from pathlib import Path
import argparse
import sys

from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand

path_to_config = str(Path(__file__).parent)

config_per_eras = {
    "2016APV": {
        "mc": "RunIISummer20UL16NanoAODAPVv9_cfg.py",
    },
    "2016": {
        "mc": "RunIISummer20UL16NanoAODv9_cfg.py",
    },
    "2017": {
        "mc": "RunIISummer20UL17NanoAODv9_cfg.py",
    },
    "2018": {
        "mc": "RunIISummer20UL18NanoAODv9_cfg.py",
    },
    "2022": {
        "mc": "Run3Summer22NanoAODv12_cfg.py",
        "data": "Run2022C-E-22Sep2023NanoAODv12_cfg.py",
    },
    "2022EE": {
        "mc": "Run3Summer22EENanoAODv12_cfg.py",
        "data-C-E": "Run2022C-E-22Sep2023NanoAODv12_cfg.py",
        "data-F-G": "Run2022F-G-22Sep2023NanoAODv12_cfg.py",
    },
    "2023-pre-Bpix": {
        "mc": "Run3Summer23NanoAODv12_cfg.py",
        "data": "Run2023-22Sep2023NanoAODv12_cfg.py",
    },
    "2023-Bpix": {
        "mc": "Run3Summer23BPixNanoAODv12_cfg.py",
        "data": "Run2023-22Sep2023NanoAODv12_cfg.py",
    },
}

# list of miniaod samples
# comment ununsed lines
all_samples = {
    "2016APV": {
        "mc": {
            "XtoYH": {
                "NMSSM_XToYH_HTo2bYTo2t_MX2000_MY400": "NMSSM_XToYH_HTo2bYTo2t_MX2000_MY400/mrogulji-PrivateMC-93281a9a3536c904fea2eba805b5fcef/USER"
            }
        }
    },
    "2016": {
        "mc": {
            "XtoYH": {
                "NMSSM_XToYH_HTo2bYTo2t_MX2000_MY400": "/NMSSM_XToYH_HTo2bYTo2t_MX2000_MY400/mrogulji-PrivateMC-a71ce5bd7a29e4e0732d62e00a2b7f74/USER"
            }
        }
    },
    "2017": {
        "mc": {
            "XtoYH": {
                "NMSSM_XToYH_HTo2bYTo2t_MX2000_MY400": "/NMSSM_XToYH_HTo2bYTo2t_MX2000_MY400/mrogulji-PrivateMC-c15273f0b6812ff053a850f456209388/USER"
            }
        }
    },
    "2018": {
        "mc": {
            "XtoYH": {
                "NMSSM_XToYH_HTo2bYTo2t_MX2000_MY400": "/NMSSM_XToYH_HTo2bYTo2t_MX2000_MY400/mrogulji-PrivateMC-f268068ea718e1e214ef739dd7f578ce/USER"
            }
        }
    }
}

def main(args):
    username = args.username
    era = args.era
    key = args.key

    samples = all_samples[era][key]
    config_name = config_per_eras[era][key]

    for sample, dataset_dict in samples.items():
        for dataset, dataset_path in dataset_dict.items():
            this_config = config()
            this_config.section_('General')
            this_config.General.workArea = 'crab/nanoaod_v12/'
            this_config.General.transferOutputs = True
            this_config.General.transferLogs = True
            this_config.General.requestName = f'nanoaod_v12_legacy_{era}_{dataset}'
            
            this_config.section_('JobType')
            this_config.JobType.psetName = f'{path_to_config}/{config_name}'
            this_config.JobType.pluginName = 'Analysis'
            this_config.JobType.numCores = 2
            this_config.JobType.allowUndistributedCMSSW = True
            this_config.JobType.maxMemoryMB = 5000
            
            this_config.section_('Data')
            this_config.Data.inputDataset = dataset_path
            this_config.Data.outputDatasetTag = dataset
            this_config.Data.publication = True
            this_config.Data.inputDBS = 'global'
            this_config.Data.splitting = 'Automatic'
            this_config.Data.outLFNDirBase = f'/store/user/{username}/MatejPFNano/{era}/{sample}'
            this_config.Data.lumiMask = ''
            
            this_config.section_('Site')
            this_config.Site.storageSite = 'T3_US_FNALLPC'
            
            this_config.section_('User')
            this_config.section_('Debug')
            
            print(this_config)
            crabCommand('submit', config=this_config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--era",
        choices=list(config_per_eras.keys()),
        required=True,
        help="era",
        type=str,
    )
    parser.add_argument(
        "--key",
        choices=["data","mc","data-C-E","data-F-G"],
        required=True,
        help="key data or mc",
        type=str,
    )
    parser.add_argument(
        "--username",
        required=True,
        type=str,
        help="username"
    )
    args = parser.parse_args()

    sys.exit(main(args))
