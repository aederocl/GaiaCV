from gaiaxpy import calibrate
from astroquery.gaia import Gaia
from astropy.io import fits 
import numpy as np

# username: aedero01

n = 100

adql = f"""
SELECT
top {n}
    g.source_id,
    g.ra, g.dec,
    g.parallax, g.parallax_error,
    g.phot_g_mean_mag,
    g.phot_g_mean_flux, g.phot_g_mean_flux_error,
    g.phot_bp_mean_mag,
    g.phot_bp_mean_flux, g.phot_bp_mean_flux_error,
    g.phot_rp_mean_mag,
    g.phot_rp_mean_flux, g.phot_rp_mean_flux_error,
    g.bp_rp,
    g.ruwe,
    g.phot_bp_rp_excess_factor,
    g.visibility_periods_used,
    g.duplicated_source,
    v.num_selected_g_fov,
    v.std_dev_mag_g_fov,
    v.skewness_mag_g_fov,
    v.kurtosis_mag_g_fov,
    v.mad_mag_g_fov,
    v.abbe_mag_g_fov,
    v.iqr_mag_g_fov,
    v.stetson_mag_g_fov,
    v.std_dev_over_rms_err_mag_g_fov
    FROM gaiadr3.gaia_source AS g
    JOIN gaiadr3.vari_summary AS v on v.source_id = g.source_id
    where g.has_xp_continuous = 'True' and g.has_epoch_photometry = 'True'
    ORDER BY g.phot_g_mean_mag ASC"""

print(adql)

job = Gaia.launch_job(adql,dump_to_file=True, output_format='fits')
fitsFileName = job.outputFile
print(job)


hdul = fits.open(fitsFileName)

hdul.info()

table = hdul[1].data
source_ids = table['source_id'].tolist()
print(source_ids)

sampling = np.arange(336., 1021., 2.) 
calibrated_spectra = calibrate(source_ids,sampling=sampling,truncation=True,output_file='my_file', output_format='fits',save_file=True)
