# # Multi-modal batch correction
# nohup python main.py --multirun +experiment=multimodal_PBMC_base_ablation +cluster=slurm >> PBMC_bc.log 2>&1 &
# nohup python main.py --multirun +experiment=multimodal_PBMC_base_ablation_qr +cluster=slurm >> PBMC_qr.log 2>&1 &

# # Multi-modal cell-typing
# nohup python main.py --multirun +experiment=multimodal_Neurips_base_ablation +cluster=slurm >> Neurips_bc.log 2>&1 &
# nohup python main.py --multirun +experiment=multimodal_Neurips_base_ablation_qr +cluster=slurm >> Neurips_qr.log 2>&1 &

# # Temperature
# nohup python main.py --multirun +experiment=multimodal_PBMC_base_ablation_temp +cluster=slurm >> PBMC_temp.log 2>&1 &
# nohup python main.py --multirun +experiment=multimodal_Neurips_base_ablation_temp +cluster=slurm >> Neurips_temp.log 2>&1 &

# nohup python main.py --multirun +experiment=multimodal_Neurips_base_ablation_temp_left +cluster=slurm >> Neurips_temp_left.log 2>&1 &

# nohup python main.py --multirun +experiment=temperature_single_modality_experiment +cluster=slurm >> unimodal_temp.log 2>&1 &

# # Single-modal projection
# nohup python main.py --multirun +experiment=unimodal_projection_no +cluster=slurm >> unimodal_projection_no.log 2>&1 &
# nohup python main.py --multirun +experiment=unimodal_projection_yes +cluster=slurm >> unimodal_projection_yes.log 2>&1 &

# # Cell typing
# nohup python main.py --multirun +experiment=unimodal_qr_b2 +cluster=slurm >> unimodal_qr_b2.log 2>&1 &
# nohup python main.py --multirun +experiment=unimodal_qr_b3 +cluster=slurm >> unimodal_qr_b3.log 2>&1 &
# nohup python main.py --multirun +experiment=unimodal_qr_b4 +cluster=slurm >> unimodal_qr_b4.log 2>&1 &
# nohup python main.py --multirun +experiment=unimodal_qr_b5 +cluster=slurm >> unimodal_qr_b5.log 2>&1 &

# nohup python main.py --multirun +exp=qr_big +cluster=slurm >> qr_big.log 2>&1 &

# Augmentations
nohup python main.py --multirun +aug_exp=bbknn_ablation +cluster=slurm >> bbknn_qr_b2.log 2>&1 &
nohup python main.py --multirun +aug_exp=combi-bbknn-all +cluster=slurm >> combi_bbknn_qr_b2.log 2>&1 &
nohup python main.py --multirun +aug_exp=combi-gauss-all +cluster=slurm >> combi_gauss_qr_b2.log 2>&1 &
nohup python main.py --multirun +aug_exp=combi-mask-all +cluster=slurm >> combi_mask_qr_b2.log 2>&1 &
nohup python main.py --multirun +aug_exp=combi-swap-all +cluster=slurm >> combi_swap_qr_b2.log 2>&1 &
nohup python main.py --multirun +aug_exp=gauss_ablation +cluster=slurm >> gauss_ablation.log 2>&1 &
nohup python main.py --multirun +aug_exp=innerswap_ablation +cluster=slurm >> innerswap_ablation.log 2>&1 &
nohup python main.py --multirun +aug_exp=mask_ablation +cluster=slurm >> mask_ablation.log 2>&1 &
nohup python main.py --multirun +aug_exp=mnn_ablation +cluster=slurm >> mnn_ablation.log 2>&1 &
