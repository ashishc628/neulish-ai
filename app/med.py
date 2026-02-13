import numpy as np
from scipy.io import wavfile
from scipy import signal
import os


# ==================== RAIN SOUND GENERATION ====================

def generate_rain_sound(duration_seconds=900, sample_rate=44100, output_file="gentle_rain.wav"):
    """
    Generate a gentle, realistic rain sound for sleep meditation.

    Parameters:
    - duration_seconds: Length of audio (default 900 = 15 minutes)
    - sample_rate: Audio sample rate (44100 Hz is CD quality)
    - output_file: Name of output WAV file
    """

    print(f"Generating {duration_seconds / 60:.1f} minute rain sound...")

    # Calculate total number of samples
    num_samples = int(duration_seconds * sample_rate)

    # Initialize empty audio array
    rain = np.zeros(num_samples)

    # LAYER 1: Individual raindrops (random impulses)
    drop_density = 0.003  # Probability of raindrop per sample (gentle rain)
    drop_positions = np.random.random(num_samples) < drop_density
    drop_amplitudes = np.random.random(num_samples) * 0.15

    raindrops = drop_positions * drop_amplitudes

    # Apply short decay envelope to each raindrop
    decay_length = int(0.02 * sample_rate)  # 20ms decay
    decay_env = np.exp(-np.linspace(0, 5, decay_length))
    raindrops = np.convolve(raindrops, decay_env, mode='same')

    rain += raindrops

    # LAYER 2: Pink noise (continuous rainfall texture)
    white_noise = np.random.randn(num_samples)
    pink_noise = apply_pink_filter(white_noise)
    pink_noise = pink_noise * 0.08

    rain += pink_noise

    # LAYER 3: Low rumble (distant rain on roof/ground)
    rumble_freq = 0.5  # Hz
    t = np.linspace(0, duration_seconds, num_samples)
    rumble = np.sin(2 * np.pi * rumble_freq * t) * 0.03
    rumble += np.random.randn(num_samples) * 0.02
    rumble = apply_lowpass_filter(rumble, cutoff=200, sample_rate=sample_rate)

    rain += rumble

    # LAYER 4: Gentle splashes
    splash_density = 0.0005
    splash_positions = np.random.random(num_samples) < splash_density
    splash_amplitudes = np.random.random(num_samples) * 0.25

    splashes = splash_positions * splash_amplitudes
    splash_decay_length = int(0.08 * sample_rate)
    splash_decay = np.exp(-np.linspace(0, 4, splash_decay_length))
    splashes = np.convolve(splashes, splash_decay, mode='same')

    rain += splashes

    # Apply gentle fade in (45 seconds)
    fade_in_samples = int(45 * sample_rate)
    fade_in = np.linspace(0, 1, fade_in_samples)
    rain[:fade_in_samples] *= fade_in

    # Apply gentle fade out (60 seconds)
    fade_out_samples = int(60 * sample_rate)
    fade_out = np.linspace(1, 0, fade_out_samples)
    rain[-fade_out_samples:] *= fade_out

    # Apply bandpass filter
    rain = apply_bandpass_filter(rain, low=100, high=8000, sample_rate=sample_rate)

    # Normalize and reduce volume
    max_val = np.max(np.abs(rain))
    if max_val > 0:
        rain = rain / max_val
    rain = rain * 0.04  # -28dB for background

    # Convert to 16-bit PCM
    rain_16bit = np.int16(rain * 32767)

    # Save to WAV file
    wavfile.write(output_file, sample_rate, rain_16bit)

    print(f"✓ Rain sound saved to '{output_file}'")

    return output_file


# ==================== SINGING BOWL GENERATION ====================

def generate_singing_bowl(duration_seconds=30, sample_rate=44100,
                          fundamental_freq=256, bowl_type="tibetan",
                          output_file="singing_bowl.wav"):
    """
    Generate a realistic singing bowl sound with natural harmonics and decay.

    Parameters:
    - duration_seconds: Length of the bowl sound
    - sample_rate: Audio sample rate
    - fundamental_freq: Base frequency (C4=256Hz, D4=293Hz, E4=330Hz, etc.)
    - bowl_type: "tibetan" (warmer, more harmonics) or "crystal" (purer, clearer)
    - output_file: Name of output WAV file
    """

    print(f"Generating {bowl_type} singing bowl at {fundamental_freq}Hz...")

    num_samples = int(duration_seconds * sample_rate)
    t = np.linspace(0, duration_seconds, num_samples)

    # Initialize the bowl sound
    bowl = np.zeros(num_samples)

    # Define harmonic series based on bowl type
    if bowl_type == "tibetan":
        # Tibetan bowls have rich, complex harmonics
        harmonics = [
            (1.0, 1.0, 3.0),  # Fundamental (frequency_mult, amplitude, decay_rate)
            (2.01, 0.7, 4.5),  # Slightly detuned 2nd harmonic
            (3.02, 0.5, 5.0),  # Slightly detuned 3rd harmonic
            (4.03, 0.3, 5.5),  # 4th harmonic
            (5.05, 0.2, 6.0),  # 5th harmonic
            (6.08, 0.15, 6.5),  # 6th harmonic
            (7.1, 0.1, 7.0),  # 7th harmonic
            (8.15, 0.08, 7.5),  # 8th harmonic
        ]
        # Add warbling (slow frequency modulation for warmth)
        warble_amount = 0.003
        warble_freq = 4.5  # Hz

    else:  # crystal bowl
        # Crystal bowls have cleaner, purer harmonics
        harmonics = [
            (1.0, 1.0, 4.0),  # Fundamental
            (2.0, 0.4, 5.0),  # Perfect 2nd harmonic
            (3.0, 0.2, 6.0),  # Perfect 3rd harmonic
            (4.0, 0.1, 7.0),  # Perfect 4th harmonic
            (5.0, 0.05, 8.0),  # Perfect 5th harmonic
        ]
        # Less warbling for crystal clarity
        warble_amount = 0.001
        warble_freq = 3.0

    # Generate each harmonic
    for freq_mult, amplitude, decay_rate in harmonics:
        harmonic_freq = fundamental_freq * freq_mult

        # Add slight frequency modulation (warbling/beating)
        modulation = 1 + warble_amount * np.sin(2 * np.pi * warble_freq * t)

        # Generate the tone with modulation
        harmonic_wave = amplitude * np.sin(2 * np.pi * harmonic_freq * modulation * t)

        # Apply exponential decay envelope
        decay_envelope = np.exp(-decay_rate * t / duration_seconds)

        # Add to bowl sound
        bowl += harmonic_wave * decay_envelope

    # Add subtle noise for realism (the "shimmer")
    noise = np.random.randn(num_samples) * 0.005
    noise_envelope = np.exp(-8 * t / duration_seconds)
    bowl += noise * noise_envelope

    # Apply gentle attack (initial strike)
    attack_samples = int(0.05 * sample_rate)  # 50ms attack
    attack_env = np.linspace(0, 1, attack_samples)
    bowl[:attack_samples] *= attack_env

    # Add slight resonance wobble (beating effect)
    beat_freq = 0.7  # Hz
    beat_amount = 0.02
    beat_envelope = np.exp(-3 * t / duration_seconds)
    beating = 1 + beat_amount * np.sin(2 * np.pi * beat_freq * t) * beat_envelope
    bowl *= beating

    # Normalize
    max_val = np.max(np.abs(bowl))
    if max_val > 0:
        bowl = bowl / max_val

    # Apply gentle compression for smoothness
    bowl = np.tanh(bowl * 1.2) * 0.8

    # Convert to 16-bit PCM
    bowl_16bit = np.int16(bowl * 32767)

    # Save to WAV file
    wavfile.write(output_file, sample_rate, bowl_16bit)

    print(f"✓ Singing bowl saved to '{output_file}'")

    return output_file


def generate_bowl_sequence(total_duration=900, interval=120, sample_rate=44100,
                           bowl_type="tibetan", output_file="bowl_sequence.wav"):
    """
    Generate a sequence of singing bowls at regular intervals.

    Parameters:
    - total_duration: Total length in seconds (e.g., 900 = 15 minutes)
    - interval: Seconds between each bowl strike (e.g., 120 = every 2 minutes)
    - sample_rate: Audio sample rate
    - bowl_type: "tibetan" or "crystal"
    - output_file: Name of output WAV file
    """

    print(f"\nGenerating bowl sequence: {total_duration / 60:.1f} min with bowls every {interval}s...")

    num_samples = int(total_duration * sample_rate)
    sequence = np.zeros(num_samples)

    # Define a set of complementary frequencies (healing frequencies)
    if bowl_type == "tibetan":
        frequencies = [256, 288, 320, 256, 288]  # C, D, E pattern
    else:  # crystal
        frequencies = [256, 384, 512, 256, 384]  # C, G, C octave pattern

    # Place bowls at intervals
    bowl_times = np.arange(0, total_duration, interval)

    for i, strike_time in enumerate(bowl_times):
        # Select frequency from pattern
        freq = frequencies[i % len(frequencies)]

        # Generate individual bowl
        bowl_duration = min(45, interval - 5)  # Long decay, but don't overlap much
        bowl = generate_single_bowl(
            duration=bowl_duration,
            frequency=freq,
            sample_rate=sample_rate,
            bowl_type=bowl_type
        )

        # Calculate position in sequence
        start_sample = int(strike_time * sample_rate)
        end_sample = min(start_sample + len(bowl), num_samples)
        bowl_length = end_sample - start_sample

        # Add to sequence
        sequence[start_sample:end_sample] += bowl[:bowl_length]

    # Normalize
    max_val = np.max(np.abs(sequence))
    if max_val > 0:
        sequence = sequence / max_val

    sequence = sequence * 0.6  # Reduce overall volume

    # Convert to 16-bit PCM
    sequence_16bit = np.int16(sequence * 32767)

    # Save to WAV file
    wavfile.write(output_file, sample_rate, sequence_16bit)

    print(f"✓ Bowl sequence saved to '{output_file}'")
    print(f"  Number of bowls: {len(bowl_times)}")

    return output_file


def generate_single_bowl(duration, frequency, sample_rate, bowl_type):
    """Helper function to generate a single bowl sound (returns array, not file)"""

    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples)
    bowl = np.zeros(num_samples)

    if bowl_type == "tibetan":
        harmonics = [
            (1.0, 1.0, 3.0),
            (2.01, 0.7, 4.5),
            (3.02, 0.5, 5.0),
            (4.03, 0.3, 5.5),
            (5.05, 0.2, 6.0),
        ]
        warble_amount = 0.003
        warble_freq = 4.5
    else:
        harmonics = [
            (1.0, 1.0, 4.0),
            (2.0, 0.4, 5.0),
            (3.0, 0.2, 6.0),
            (4.0, 0.1, 7.0),
        ]
        warble_amount = 0.001
        warble_freq = 3.0

    for freq_mult, amplitude, decay_rate in harmonics:
        harmonic_freq = frequency * freq_mult
        modulation = 1 + warble_amount * np.sin(2 * np.pi * warble_freq * t)
        harmonic_wave = amplitude * np.sin(2 * np.pi * harmonic_freq * modulation * t)
        decay_envelope = np.exp(-decay_rate * t / duration)
        bowl += harmonic_wave * decay_envelope

    # Attack envelope
    attack_samples = int(0.05 * sample_rate)
    attack_env = np.linspace(0, 1, attack_samples)
    bowl[:attack_samples] *= attack_env

    # Normalize
    max_val = np.max(np.abs(bowl))
    if max_val > 0:
        bowl = bowl / max_val

    return bowl


# ==================== HELPER FUNCTIONS ====================

def apply_pink_filter(white_noise):
    """Convert white noise to pink noise using FFT"""
    fft = np.fft.rfft(white_noise)
    frequencies = np.fft.rfftfreq(len(white_noise))
    frequencies[0] = 1  # Avoid division by zero
    pink_spectrum = fft / np.sqrt(frequencies)
    pink_noise = np.fft.irfft(pink_spectrum, n=len(white_noise))
    return pink_noise


def apply_lowpass_filter(audio, cutoff=200, sample_rate=44100):
    """Apply low-pass filter to keep only low frequencies"""
    nyquist = sample_rate / 2
    normalized_cutoff = cutoff / nyquist
    b, a = signal.butter(4, normalized_cutoff, btype='low')
    filtered = signal.filtfilt(b, a, audio)
    return filtered


def apply_bandpass_filter(audio, low=100, high=8000, sample_rate=44100):
    """Apply band-pass filter to keep frequencies in specified range"""
    nyquist = sample_rate / 2
    normalized_low = low / nyquist
    normalized_high = high / nyquist
    b, a = signal.butter(3, [normalized_low, normalized_high], btype='band')
    filtered = signal.filtfilt(b, a, audio)
    return filtered


def combine_audio_files(file1, file2, output_file, volume1=1.0, volume2=1.0):
    """
    Combine two audio files (e.g., rain + bowls)

    Parameters:
    - file1: First audio file (e.g., rain)
    - file2: Second audio file (e.g., bowls)
    - output_file: Combined output file
    - volume1: Volume multiplier for file1 (0.0 to 1.0)
    - volume2: Volume multiplier for file2 (0.0 to 1.0)
    """

    print(f"\nCombining {file1} and {file2}...")

    # Read both files
    rate1, audio1 = wavfile.read(file1)
    rate2, audio2 = wavfile.read(file2)

    # Ensure same sample rate
    if rate1 != rate2:
        print(f"Warning: Sample rates differ ({rate1} vs {rate2})")
        return None

    # Convert to float
    audio1 = audio1.astype(np.float32) / 32768.0
    audio2 = audio2.astype(np.float32) / 32768.0

    # Match lengths (pad shorter one with zeros)
    max_length = max(len(audio1), len(audio2))
    if len(audio1) < max_length:
        audio1 = np.pad(audio1, (0, max_length - len(audio1)))
    if len(audio2) < max_length:
        audio2 = np.pad(audio2, (0, max_length - len(audio2)))

    # Apply volume multipliers
    audio1 = audio1 * volume1
    audio2 = audio2 * volume2

    # Combine
    combined = audio1 + audio2

    # Normalize to prevent clipping
    max_val = np.max(np.abs(combined))
    if max_val > 0.95:
        combined = combined * (0.95 / max_val)

    # Convert back to 16-bit
    combined_16bit = np.int16(combined * 32767)

    # Save
    wavfile.write(output_file, rate1, combined_16bit)

    print(f"✓ Combined audio saved to '{output_file}'")

    return output_file


# ==================== MAIN GENERATION FUNCTIONS ====================

def generate_complete_meditation_set():
    """
    Generate a complete set of meditation sounds:
    - Rain backgrounds for different durations
    - Individual singing bowls
    - Bowl sequences
    - Combined rain + bowl tracks
    """

    print("\n" + "=" * 60)
    print("MEDITATION SOUND GENERATION SUITE")
    print("=" * 60 + "\n")

    # Create output directory
    os.makedirs("meditation_sounds", exist_ok=True)
    os.chdir("meditation_sounds")

    # ===== RAIN SOUNDS =====
    print("\n--- GENERATING RAIN SOUNDS ---\n")

    rain_5min = generate_rain_sound(300, output_file="rain_5min.wav")
    rain_7min = generate_rain_sound(420, output_file="rain_7min.wav")
    rain_9min = generate_rain_sound(540, output_file="rain_9min.wav")
    rain_15min = generate_rain_sound(900, output_file="rain_15min.wav")

    # ===== SINGING BOWLS =====
    print("\n--- GENERATING SINGING BOWLS ---\n")

    # Tibetan bowls at different frequencies
    generate_singing_bowl(30, fundamental_freq=256, bowl_type="tibetan",
                          output_file="tibetan_bowl_C.wav")
    generate_singing_bowl(30, fundamental_freq=288, bowl_type="tibetan",
                          output_file="tibetan_bowl_D.wav")
    generate_singing_bowl(30, fundamental_freq=320, bowl_type="tibetan",
                          output_file="tibetan_bowl_E.wav")

    # Crystal bowls at different frequencies
    generate_singing_bowl(30, fundamental_freq=256, bowl_type="crystal",
                          output_file="crystal_bowl_C.wav")
    generate_singing_bowl(30, fundamental_freq=384, bowl_type="crystal",
                          output_file="crystal_bowl_G.wav")
    generate_singing_bowl(30, fundamental_freq=512, bowl_type="crystal",
                          output_file="crystal_bowl_C_high.wav")

    # ===== BOWL SEQUENCES =====
    print("\n--- GENERATING BOWL SEQUENCES ---\n")

    # Tibetan bowl sequence - every 2 minutes for 15 minutes
    generate_bowl_sequence(900, interval=120, bowl_type="tibetan",
                           output_file="tibetan_sequence_15min.wav")

    # Crystal bowl sequence - every 90 seconds for 9 minutes
    generate_bowl_sequence(540, interval=90, bowl_type="crystal",
                           output_file="crystal_sequence_9min.wav")

    # ===== COMBINED TRACKS =====
    print("\n--- GENERATING COMBINED TRACKS ---\n")

    # Rain + Tibetan bowls (15 min)
    combine_audio_files("rain_15min.wav", "tibetan_sequence_15min.wav",
                        "rain_tibetan_bowls_15min.wav",
                        volume1=0.7, volume2=0.5)

    # Rain + Crystal bowls (9 min)
    combine_audio_files("rain_9min.wav", "crystal_sequence_9min.wav",
                        "rain_crystal_bowls_9min.wav",
                        volume1=0.7, volume2=0.5)

    print("\n" + "=" * 60)
    print("✓ ALL MEDITATION SOUNDS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nFiles saved in: {os.getcwd()}")
    print("\nGenerated files:")
    print("\nRAIN BACKGROUNDS:")
    print("  - rain_5min.wav")
    print("  - rain_7min.wav")
    print("  - rain_9min.wav")
    print("  - rain_15min.wav")
    print("\nTIBETAN BOWLS:")
    print("  - tibetan_bowl_C.wav")
    print("  - tibetan_bowl_D.wav")
    print("  - tibetan_bowl_E.wav")
    print("  - tibetan_sequence_15min.wav")
    print("\nCRYSTAL BOWLS:")
    print("  - crystal_bowl_C.wav")
    print("  - crystal_bowl_G.wav")
    print("  - crystal_bowl_C_high.wav")
    print("  - crystal_sequence_9min.wav")
    print("\nCOMBINED TRACKS:")
    print("  - rain_tibetan_bowls_15min.wav")
    print("  - rain_crystal_bowls_9min.wav")
    print("\n")


if __name__ == "__main__":
    generate_complete_meditation_set()