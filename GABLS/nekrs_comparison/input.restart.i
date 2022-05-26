#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#            SIMULATION STOP            #
#.......................................#
time.stop_time               = 36000.0  # Max (simulated) time to evolve
time.max_step                = 461800   # Max number of time steps


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#         TIME STEP COMPUTATION         #
#.......................................#
time.fixed_dt         =   0.0625        # Use this constant dt if > 0
time.cfl              =   0.95          # CFL factor


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#            INPUT AND OUTPUT           #
#.......................................#
io.restart_file = "chk460800"
time.plot_interval            =  -16000  # Steps between plot files
time.checkpoint_interval      =  -16000  # Steps between checkpoint files


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#               PHYSICS                 #
#.......................................#
incflo.gravity        =  0.0  0.0 -9.81  # Gravitational force (3D)
incflo.density        =  1.3223            # Reference density
incflo.use_godunov = 1
incflo.godunov_type = weno_z
transport.viscosity = 1.0E-5
transport.laminar_prandtl = 0.7
transport.turbulent_prandtl = 0.3333
turbulence.model = Smagorinsky
Smagorinsky_coeffs.Cs = 0.135
incflo.physics = ABL
ICNS.source_terms = BoussinesqBuoyancy CoriolisForcing GeostrophicForcing
#TKE.source_terms = KsgsM84Src
BoussinesqBuoyancy.reference_temperature = 263.5
CoriolisForcing.east_vector = 1.0 0.0 0.0
CoriolisForcing.north_vector = 0.0 1.0 0.0
CoriolisForcing.latitude = 90.0
CoriolisForcing.rotational_time_period = 90405.5439881955
GeostrophicForcing.geostrophic_wind = 8.0 0.0 0.0
incflo.velocity = 8.0 0.0 0.0
ABL.reference_temperature = 263.5
ABL.temperature_heights = 0.0 100 400.0
ABL.temperature_values = 265.0 265.0 268.0
ABL.perturb_temperature = true
ABL.cutoff_height = 50.0
ABL.perturb_velocity = false
ABL.perturb_ref_height = 50.0
ABL.Uperiods = 4.0
ABL.Vperiods = 4.0
ABL.deltaU = 1e-5
ABL.deltaV = 1e-5
ABL.kappa = .40
ABL.mo_gamma_m = 4.8
ABL.mo_gamma_h = 7.8
ABL.surface_roughness_z0 = 0.1
ABL.surface_temp_rate = -0.25
ABL.surface_temp_init = 265.0
ABL.normal_direction = 2
ABL.stats_output_frequency = 10000
#ABL.stats_output_format = netcdf


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#        ADAPTIVE MESH REFINEMENT       #
#.......................................#
amr.n_cell              = 512 512 512 # Grid cells at coarsest AMRlevel
amr.max_level           = 0           # Max AMR level in hierarchy
amr.max_grid_size       = 128


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#              GEOMETRY                 #
#.......................................#
geometry.prob_lo        =   0.       0.     0.  # Lo corner coordinates
geometry.prob_hi        =   400.   400.   400.  # Hi corner coordinates
geometry.is_periodic    =   1   1   0   # Periodicity x y z (0/1)
# Boundary conditions
zlo.type =   "wall_model"
zlo.temperature_type = "wall_model"
zhi.type =   "slip_wall"
zhi.temperature_type = "fixed_gradient"
zhi.temperature = 0.01
zlo.tke_type = "zero_gradient"
#zhi.tke_type = "zero_gradient"
incflo.verbose          =   0


#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨#
#              MLMG SETTINGS            #
#.......................................#
nodal_proj.mg_rtol = 1.0e-4
nodal_proj.mg_atol = 1.0e-12
mac_proj.mg_rtol = 1.0e-4
mac_proj.mg_atol = 1.0e-12
diffusion.max_coarsening_level=0
diffusion.bottom_solver=bicg
velocity_diffusion.use_tensor_operator=false
diffusion.mg_rtol = 1.0e-6
diffusion.mg_atol = 1.0e-12
temperature_diffusion.mg_rtol = 1.0e-6
temperature_diffusion.mg_atol = 1.0e-13


