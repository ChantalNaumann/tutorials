"""
neurodata.py - fake (but realistic-looking) neuroscience data for the plotting course.

You do NOT need to understand this file to follow the course. Every function
returns plain NumPy arrays so that we can focus on *plotting*.
Every function takes a `seed`, so everyone in the room gets the same "random" data.

    import neurodata
    t, v, current, spikes = neurodata.membrane_potential()
    help(neurodata.membrane_potential)   # read what a function returns
"""
import numpy as np


def membrane_potential(duration=1.0, dt=1e-4, stim_on=0.2, stim_off=0.8,
                       stim_amp=1.8, seed=0):
    """Leaky integrate-and-fire neuron driven by a noisy current step.

    Returns
    -------
    t : time in seconds, shape (n,)
    v : membrane potential in mV, shape (n,)
    current : injected current in nA, shape (n,)
    spike_times : spike times in seconds, shape (k,)
    """
    rng = np.random.default_rng(seed)
    tau, resistance = 0.02, 15.0  # s, MOhm
    v_rest, v_threshold, v_reset = -70.0, -50.0, -72.0

    t = np.arange(0, duration, dt)
    current = np.where((t >= stim_on) & (t < stim_off), stim_amp, 0.0)
    noise = rng.normal(0, 4.0 * np.sqrt(dt / tau), t.size)

    v = np.full_like(t, v_rest)
    spike_times = []
    for i in range(1, t.size):
        dv = (-(v[i - 1] - v_rest) + resistance * current[i - 1]) * dt / tau
        v[i] = v[i - 1] + dv + noise[i]
        if v[i] >= v_threshold:
            v[i - 1] = 20.0  # draw the action potential
            v[i] = v_reset
            spike_times.append(t[i])
    return t, v, current, np.array(spike_times)


def spike_trains(n_trials=30, duration=2.0, stim_on=0.5, stim_off=1.5,
                 baseline_rate=5.0, peak_rate=60.0, sustained_rate=20.0, seed=0):
    """Spike trains of one neuron over repeated trials of a stimulus.

    The neuron fires at `baseline_rate` (Hz), responds to the stimulus with a
    transient peak that decays to a sustained rate, and returns to baseline.

    Returns
    -------
    trials : list with one array of spike times (s) per trial
    """
    rng = np.random.default_rng(seed)
    dt = 1e-3
    t = np.arange(0, duration, dt)
    rate = np.full_like(t, baseline_rate)
    during = (t >= stim_on) & (t < stim_off)
    since_onset = t[during] - stim_on
    rate[during] = sustained_rate + (peak_rate - sustained_rate) * np.exp(-since_onset / 0.08)

    trials = []
    for _ in range(n_trials):
        gain = rng.gamma(20, 1 / 20)  # trial-to-trial variability
        fired = rng.random(t.size) < rate * gain * dt
        trials.append(np.sort(t[fired] + rng.uniform(0, dt, fired.sum())))
    return trials


def orientation_tuning(n_neurons=4, n_trials=12, seed=0):
    """Responses of V1-like neurons to oriented gratings.

    Returns
    -------
    orientations : grating orientations in degrees, shape (12,)
    responses : spike counts, shape (n_neurons, n_orientations, n_trials)
    """
    rng = np.random.default_rng(seed)
    orientations = np.arange(0, 180, 15.0)
    preferred = rng.uniform(0, 180, n_neurons)
    peak = rng.uniform(15, 40, n_neurons)
    base = rng.uniform(1, 5, n_neurons)
    width = rng.uniform(1.5, 4, n_neurons)

    angle = np.deg2rad(orientations[None, :] - preferred[:, None]) * 2
    mean = base[:, None] + peak[:, None] * np.exp(width[:, None] * (np.cos(angle) - 1))
    responses = rng.poisson(mean[:, :, None], size=(n_neurons, orientations.size, n_trials))
    return orientations, responses.astype(float)


def calcium_imaging(n_neurons=60, duration=120.0, fs=15.0, seed=0):
    """Two-photon calcium imaging: dF/F traces of many neurons.

    About 40 % of the neurons respond to a stimulus presented every 15 s.

    Returns
    -------
    t : time in seconds, shape (n_frames,)
    dff : dF/F, shape (n_neurons, n_frames)
    stim_times : stimulus onset times in seconds
    """
    rng = np.random.default_rng(seed)
    t = np.arange(0, duration, 1 / fs)
    stim_times = np.arange(10, duration - 5, 15.0)

    rates = rng.lognormal(np.log(0.1), 0.8, n_neurons)  # spontaneous rate, Hz
    spikes = rng.poisson(rates[:, None] / fs, (n_neurons, t.size)).astype(float)
    responsive = rng.random(n_neurons) < 0.4
    latency = rng.uniform(0, 2, n_neurons)
    for i in np.flatnonzero(responsive):
        for s in stim_times:
            start = int((s + latency[i]) * fs)
            spikes[i, start:start + 3] += rng.poisson(2, 3)

    kernel_t = np.arange(0, 5, 1 / fs)
    kernel = (1 - np.exp(-kernel_t / 0.1)) * np.exp(-kernel_t / 1.0)  # GCaMP-like
    kernel /= kernel.max()
    dff = np.array([np.convolve(s, kernel)[:t.size] for s in spikes]) * 0.3
    dff += rng.normal(0, 0.05, dff.shape)
    return t, dff, stim_times


def lfp(duration=10.0, fs=1000.0, seed=0):
    """Local field potential with 1/f background, theta (8 Hz) and
    theta-nested gamma (40 Hz).

    Returns
    -------
    t : time in seconds
    x : voltage in microvolts
    """
    rng = np.random.default_rng(seed)
    t = np.arange(0, duration, 1 / fs)

    spectrum = np.fft.rfft(rng.normal(size=t.size))
    freqs = np.fft.rfftfreq(t.size, 1 / fs)
    spectrum[1:] /= np.sqrt(freqs[1:])  # 1/f power
    spectrum[0] = 0
    pink = np.fft.irfft(spectrum, n=t.size)
    pink /= pink.std()

    theta_phase = 2 * np.pi * 8 * t + np.cumsum(rng.normal(0, 0.02, t.size))
    theta = np.sin(theta_phase)
    gamma = 0.4 * (1 + np.cos(theta_phase)) / 2 * np.sin(2 * np.pi * 40 * t)
    return t, 100 * (0.8 * pink + 0.8 * theta + gamma)


def drug_experiment(n_animals=8, seed=0):
    """Mean firing rate (Hz) of one neuron per animal, before and after a drug.

    Returns
    -------
    baseline, drug : arrays of shape (n_animals,), paired by animal
    """
    rng = np.random.default_rng(seed)
    baseline = rng.normal(12, 3, n_animals)
    drug = baseline * rng.normal(0.7, 0.12, n_animals)
    return baseline, drug
