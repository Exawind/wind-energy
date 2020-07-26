# coding: utf-8
import sys
sys.path.insert(1, '../utilities')
import windspectra, load_data
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

l_cases = {
    'amrwind-ksgs': load_data.AMRWindStats('AmrWind'),
    'naluwind-smag': load_data.NaluWindStats('NaluWindRun02'),
    'naluwind-ksgs': load_data.NaluWindStats('NaluWindRun03'),
    'Pederson:2014': load_data.PedersonData('pedersen2014_data')
    }

with PdfPages('nalu_amr_comparison_n02.pdf') as pfpgs:
    plt.style.use('singleColumn')
    fig = plt.figure()
    for l,c in l_cases.items():
        plt.plot(c.hvelmag, c.z, label=l)
    plt.ylim()
    plt.xlabel(r'$< | \vec{u}_{\textrm{horiz}} | >$')
    plt.ylabel('z')
    plt.legend(loc=0)
    plt.ylim(0,750)
    plt.grid()
    plt.tight_layout()
    pfpgs.savefig()
    plt.close(fig)

    fig = plt.figure()
    for l,c in l_cases.items():
        plt.plot(c.T, c.z, label=l)
    plt.xlabel(r'$<T>$')
    plt.ylabel('z')
    plt.legend(loc=0)
    plt.ylim(0,1000)
    plt.grid()
    plt.tight_layout()
    pfpgs.savefig()
    plt.close(fig)

    plt.style.use('singleColumn.square')
    deltaX=3000.0/288         # Grid spacing
    for i, z in enumerate(l_cases['naluwind-ksgs'].ps_data['z']):
        f, suu, svv, sww = l_cases['naluwind-ksgs'].point_spectra(z)
        utau = l_cases['naluwind-ksgs'].istats['ustar']
        hvelmag = l_cases['naluwind-ksgs'].interp_hvelmag(z)
        f_a, suu_a, svv_a, sww_a = l_cases['amrwind-ksgs'].point_spectra(z)
        utau_a = float(l_cases['amrwind-ksgs'].istats['ustar'])
        fmax = 0.6*hvelmag/(8*deltaX)
        
        fig,ax = plt.subplots()
        lineu, = ax.loglog(f, windspectra.getKaimal(f, z, hvelmag ),label='Kaimal - u')
        ax.loglog(f, f * suu/(utau * utau) , '--', label='naluwind-ksgs - u')
        ax.loglog(f_a, f_a * suu_a/(utau_a * utau_a) , '-.', label='amr-wind-ksgs - u')
        plt.vlines(fmax, 5e-4, 20,lw=3, linestyle='-.')
        plt.xlim(1e-4,2)
        plt.ylim(1e-3,15)
        plt.grid()
        plt.xlabel('Frequency $f$ [Hz]')
        plt.ylabel('$f\cdot S_{u}/u_{\\tau}^2$ [-]')
        plt.title('Avg spectra [Neutral N02, z={:.1f}m]'.format(z))
        plt.legend(loc='upper right')
        plt.tight_layout()
        pfpgs.savefig()
        plt.close(fig)
        
        fig,ax = plt.subplots()
        linev, = ax.loglog(f, windspectra.getKaimal(f, z, hvelmag, params=windspectra.vKaimalconst),label='Kaimal - v')
        ax.loglog(f, f * svv/(utau * utau) , '--', label='naluwind-ksgs - v')
        ax.loglog(f_a, f_a * svv_a/(utau_a * utau_a) , '-.', label='amr-wind-ksgs - v')
        plt.vlines(fmax, 5e-4, 20,lw=3, linestyle='-.')
        plt.xlim(1e-4,2)
        plt.ylim(1e-3,15)
        plt.grid()
        plt.xlabel('Frequency $f$ [Hz]')
        plt.ylabel('$f\cdot S_{v}/u_{\\tau}^2$ [-]')
        plt.title('Avg spectra [Neutral N02, z={:.1f}m]'.format(z))
        plt.legend(loc='upper right')
        plt.tight_layout()
        pfpgs.savefig()
        plt.close(fig)
        
        fig,ax = plt.subplots()
        linew, = ax.loglog(f, windspectra.getKaimal(f, z, hvelmag, params=windspectra.wKaimalconst),label='Kaimal - w')
        ax.loglog(f, f * sww/(utau * utau) , '--', label='naluwind-ksgs - w')
        ax.loglog(f_a, f_a * sww_a/(utau_a * utau_a) , '-.', label='amr-wind-ksgs - w')
        plt.vlines(fmax, 5e-4, 20,lw=3, linestyle='-.')
        plt.xlim(1e-4,2)
        plt.ylim(1e-3,15)
        plt.grid()
        plt.xlabel('Frequency $f$ [Hz]')
        plt.ylabel('$f\cdot S_{w}/u_{\\tau}^2$ [-]')
        plt.title('Avg spectra [Neutral N02, z={:.1f}m]'.format(z))
        plt.legend(loc='upper right')
        plt.tight_layout()
        pfpgs.savefig()
        plt.close(fig)
        
