# nohup python main.py --multirun +experiment=multimodal_PBMC_base_ablation +cluster=slurm >> PBMC_bc.log 2>&1 &
# nohup python main.py --multirun +experiment=multimodal_PBMC_base_ablation_qr +cluster=slurm >> PBMC_qr.log 2>&1 &

# nohup python main.py --multirun +experiment=multimodal_Neurips_base_ablation +cluster=slurm >> Neurips_bc.log 2>&1 &
# nohup python main.py --multirun +experiment=multimodal_Neurips_base_ablation_qr +cluster=slurm >> Neurips_qr.log 2>&1 &

# nohup python main.py --multirun +experiment=multimodal_PBMC_base_ablation_temp +cluster=slurm >> PBMC_temp.log 2>&1 &
# nohup python main.py --multirun +experiment=multimodal_Neurips_base_ablation_temp +cluster=slurm >> Neurips_temp.log 2>&1 &

# nohup python main.py --multirun +experiment=multimodal_Neurips_base_ablation_temp_left +cluster=slurm >> Neurips_temp_left.log 2>&1 &

# nohup python main.py --multirun +experiment=temperature_single_modality_experiment +cluster=slurm >> unimodal_temp.log 2>&1 &

# nohup python main.py --multirun +experiment=unimodal_projection_no +cluster=slurm >> unimodal_projection_no.log 2>&1 &

# nohup python main.py --multirun +experiment=unimodal_projection_yes +cluster=slurm >> unimodal_projection_yes.log 2>&1 &

nohup python main.py --multirun +experiment=unimodal_qr_b2 +cluster=slurm >> unimodal_qr_b2.log 2>&1 &
nohup python main.py --multirun +experiment=unimodal_qr_b3 +cluster=slurm >> unimodal_qr_b3.log 2>&1 &
nohup python main.py --multirun +experiment=unimodal_qr_b4 +cluster=slurm >> unimodal_qr_b4.log 2>&1 &
nohup python main.py --multirun +experiment=unimodal_qr_b5 +cluster=slurm >> unimodal_qr_b5.log 2>&1 &

nohup python main.py --multirun +exp=qr_big +cluster=slurm >> qr_big.log 2>&1 &
