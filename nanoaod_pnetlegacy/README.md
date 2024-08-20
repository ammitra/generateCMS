# Production nanoAODv12

- Start SL7 container
```
cmssw-el7 -p --bind `readlink $HOME` --bind `readlink -f ${HOME}/nobackup/` --bind /uscms_data --bind /cvmfs
```

- Get release
```
cmsrel CMSSW_13_0_13
cd CMSSW_13_0_13/src/
cmsenv
git cms-checkout-topic cmantill:13_0_13_pNetLegacy
scram b -j 10
```

- Clone repo
```
git clone git@github.com:ammitra/generateCMS.git
cd generateCMS/nanoaod_pnetlegacy/
```

- Edit `submit_nanoaod.py` with the samples to submit

- Submit samples, specify era, key and username, e.g.:
```
python3 submit_nanoaod.py --era 2016APV --key mc --username <username>
```
