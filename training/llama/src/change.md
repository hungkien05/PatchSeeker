1) Change in datasets.py 
- Error: [rank1]: datasets.exceptions.DatasetNotFoundError: Dataset 'cve_data.json' doesn't exist on the Hub or cannot be accessed.
- Fix : 
+ Before :  
            self.data_args.dataset_name,
            self.data_args.dataset_config,
            data_files=self.data_args.dataset_name,
            split=self.data_args.dataset_split,
            cache_dir=self.data_args.dataset_cache_dir,
+ After :
            "json",  # dataset_name phải là "json" cho file cục bộ
            data_files=self.data_args.dataset_path,  # Đường dẫn tới cve_data.json
            split=self.data_args.dataset_split or "train",  # Mặc định là "train" nếu không chỉ định
            cache_dir=self.data_args.dataset_cache_dir,
(In EncodeDataset and TrainDataset)

2) Change in repllama.sh 

+           --dataset_name cve_data.json \  (load data_files above)

3) Change in driver/train.py
+ Before :     trainer.train()  # TODO: resume training
+ After :     trainer.train(resume_from_checkpoint=training_args.resume_from_checkpoint)  # TODO: resume training

4) Change in lib deepspeed
- Error: pickle.UnpicklingError: Weights only load failed. This file can still be loaded, to do so you have two options, [1mdo those steps only if you trust the source of the checkpoint[0m. 
[rank0]: 	(1) In PyTorch 2.6, we changed the default value of the `weights_only` argument in `torch.load` from `False` to `True`. Re-running `torch.load` with `weights_only` set to `False` will likely succeed, but it can result in arbitrary code execution. Do it only if you got the file from a trusted source.
[rank0]: 	(2) Alternatively, to load with `weights_only=True` please check the recommended steps in the following error message.
[rank0]: 	WeightsUnpickler error: Unsupported global: GLOBAL deepspeed.runtime.zero.config.ZeroStageEnum was not an allowed global by default. Please use `torch.serialization.add_safe_globals([ZeroStageEnum])` or the `torch.serialization.safe_globals([ZeroStageEnum])` context manager to allowlist this global if you trust this class/function.
+ Fix : set weights_only = False

+ Description ( in terminal : nano /home/huuhungn/anaconda3/envs/rankllama2/lib/python3.10/site-packages/deepspeed/runtime/checkpoint_engine/torch_checkpoint_engine.py
    in load function : partition = torch.load(path, map_location=map_location, weights_only=False))

5) Change in lib version
xformer : 0.0.29 -> 0.0.28
torch : 2.6.0 -> 2.4.1
numpy : 1.24.3 -> 2.2.4

6) Change in modeling/encoder.py
    #   llama2 7b    
    # def gradient_checkpointing_enable(self, **kwargs):
    #     self.encoder.model.gradient_checkpointing_enable()
    
    #Code reviewer
    def gradient_checkpointing_enable(self, gradient_checkpointing_kwargs= True):
        self.encoder.gradient_checkpointing_enable(gradient_checkpointing_kwargs)