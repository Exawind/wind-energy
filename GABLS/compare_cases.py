# coding: utf-8
import numpy as np
import load_data, sys
sys.path.insert(1, '../utilities')
import windspectra
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

l_cases = {
    'amrwind-ksgs-3.125m': load_data.AMRWindStats('AmrWindKsgs_3p125'),
    #'amrwind-ksgs-1.5625m': load_data.AMRWindStats('AmrWindKsgs_1p5625'),
    'GABLS: CORA': load_data.GABLSData('gabls_data/res_3.125m/CORA'),
    'GABLS: CSU': load_data.GABLSData('gabls_data/res_3.125m/CSU'),
    'GABLS: IMUK': load_data.GABLSData('gabls_data/res_3.125m/IMUK'),    
    'GABLS: LLNL': load_data.GABLSData('gabls_data/res_3.125m/LLNL'),   
    'GABLS: MO': load_data.GABLSData('gabls_data/res_3.125m/MO'),
    'GABLS: NCAR': load_data.GABLSData('gabls_data/res_3.125m/NCAR'),
    'GABLS: NERSC': load_data.GABLSData('gabls_data/res_3.125m/NERSC'),
    'GABLS: UIB': load_data.GABLSData('gabls_data/res_3.125m/UIB')
    }

with PdfPages('nalu_amr_comparison_gabls.pdf') as pfpgs:
    plt.style.use('singleColumn.square')
    #plt.style.use('singleColumn')

    fig = plt.figure()
    for l,c in l_cases.items():
        plt.plot(np.sqrt(c.u * c.u  + c.v * c.v), c.z, label=l)
    plt.ylim()
    plt.xlabel(r'$\sqrt{<u>^2 + <v>^2}$')
    plt.ylabel('z')
    plt.legend(loc=0,ncol=1)
    plt.ylim(0,300)
    plt.grid()
    plt.tight_layout()
    pfpgs.savefig()
    plt.close(fig)
    
    fig = plt.figure()
    for l,c in l_cases.items():
        plt.plot(c.u, c.z, label=l)
    plt.ylim()
    plt.xlabel(r'$<u>$')
    plt.ylabel('z')
    plt.legend(loc=0,ncol=1)
    plt.ylim(0,300)
    plt.grid()
    plt.tight_layout()
    pfpgs.savefig()
    plt.close(fig)

    fig = plt.figure()
    for l,c in l_cases.items():
        plt.plot(c.v, c.z, label=l)
    plt.ylim()
    plt.xlabel(r'$<v>$')
    plt.ylabel('z')
    plt.legend(loc=0,ncol=1)
    plt.ylim(0,300)
    plt.grid()
    plt.tight_layout()
    pfpgs.savefig()
    plt.close(fig)
    
    fig = plt.figure()
    for l,c in l_cases.items():
        plt.plot(c.T, c.z, label=l)
    plt.xlabel(r'$<T>$')
    plt.ylabel('z')
    plt.legend(loc=0,ncol=1)
    plt.ylim(0,300)
    plt.grid()
    plt.tight_layout()
    pfpgs.savefig()
    plt.close(fig)

    # plt.style.use('singleColumn.square')
    # deltaX=3000.0/288         # Grid spacing
    # for i, z in enumerate(l_cases['naluwind-ksgs'].ps_data['z']):
    #     f, suu, svv, sww = l_cases['naluwind-ksgs'].point_spectra(z)
    #     utau = l_cases['naluwind-ksgs'].istats['ustar']
    #     hvelmag = l_cases['naluwind-ksgs'].interp_hvelmag(z)
    #     f_a, suu_a, svv_a, sww_a = l_cases['amrwind-ksgs'].point_spectra(z)
    #     utau_a = float(l_cases['amrwind-ksgs'].istats['ustar'])
    #     fmax = 0.6*hvelmag/(8*deltaX)
        
    #     fig,ax = plt.subplots()
    #     lineu, = ax.loglog(f, windspectra.getKaimal(f, z, hvelmag ),label='Kaimal - u')
    #     ax.loglog(f, f * suu/(utau * utau) , '--', label='naluwind-ksgs - u')
    #     ax.loglog(f_a, f_a * suu_a/(utau_a * utau_a) , '-.', label='amr-wind-ksgs - u')
    #     plt.vlines(fmax, 5e-4, 20,lw=3, linestyle='-.')
    #     plt.xlim(1e-4,2)
    #     plt.ylim(1e-3,15)
    #     plt.grid()
    #     plt.xlabel('Frequency $f$ [Hz]')
    #     plt.ylabel('$f\cdot S_{u}/u_{\\tau}^2$ [-]')
    #     plt.title('Avg spectra [Neutral N07, z={:.1f}m]'.format(z))
    #     plt.legend(loc='upper right')
    #     plt.tight_layout()
    #     pfpgs.savefig()
    #     plt.close(fig)
        
    #     fig,ax = plt.subplots()
    #     linev, = ax.loglog(f, windspectra.getKaimal(f, z, hvelmag, params=windspectra.vKaimalconst),label='Kaimal - v')
    #     ax.loglog(f, f * svv/(utau * utau) , '--', label='naluwind-ksgs - v')
    #     ax.loglog(f_a, f_a * svv_a/(utau_a * utau_a) , '-.', label='amr-wind-ksgs - v')
    #     plt.vlines(fmax, 5e-4, 20,lw=3, linestyle='-.')
    #     plt.xlim(1e-4,2)
    #     plt.ylim(1e-3,15)
    #     plt.grid()
    #     plt.xlabel('Frequency $f$ [Hz]')
    #     plt.ylabel('$f\cdot S_{v}/u_{\\tau}^2$ [-]')
    #     plt.title('Avg spectra [Neutral N07, z={:.1f}m]'.format(z))
    #     plt.legend(loc='upper right')
    #     plt.tight_layout()
    #     pfpgs.savefig()
    #     plt.close(fig)
        
    #     fig,ax = plt.subplots()
    #     linew, = ax.loglog(f, windspectra.getKaimal(f, z, hvelmag, params=windspectra.wKaimalconst),label='Kaimal - w')
    #     ax.loglog(f, f * sww/(utau * utau) , '--', label='naluwind-ksgs - w')
    #     ax.loglog(f_a, f_a * sww_a/(utau_a * utau_a) , '-.', label='amr-wind-ksgs - w')
    #     plt.vlines(fmax, 5e-4, 20,lw=3, linestyle='-.')
    #     plt.xlim(1e-4,2)
    #     plt.ylim(1e-3,15)
    #     plt.grid()
    #     plt.xlabel('Frequency $f$ [Hz]')
    #     plt.ylabel('$f\cdot S_{w}/u_{\\tau}^2$ [-]')
    #     plt.title('Avg spectra [Neutral N07, z={:.1f}m]'.format(z))
    #     plt.legend(loc='upper right')
    #     plt.tight_layout()
    #     pfpgs.savefig()
    #     plt.close(fig)
