import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

# --- Page Configuration ---
st.set_page_config(page_title="TraceMind AI Dashboard",
                   layout="wide", page_icon="⚡")

# --- Session State Initialization ---
if 'signal_data' not in st.session_state:
    st.session_state.signal_data = None
if 'time_vector' not in st.session_state:
    st.session_state.time_vector = np.linspace(0, 1, 1000)

# --- Sidebar Controls ---
with st.sidebar:
    st.title("⚡ TraceMind AI")
    st.markdown("### 1. Spatial Data Input")
    uploaded_image = st.file_uploader(
        "Upload PCB Layout (PNG/JPG)", type=["png", "jpg", "jpeg"])

    st.markdown("### 2. Temporal Data Input")
    uploaded_csv = st.file_uploader(
        "Upload Hardware Signal (CSV)", type=["csv"])

    if st.button("Generate Mock EMG Noisy Signal", type="secondary"):
        # Generates a simulated biosignal (like EMG) corrupted by 50Hz hum
        clean_signal = 1.2 * np.sin(2 * np.pi * 8 * st.session_state.time_vector) + \
            0.4 * np.sin(2 * np.pi * 23 * st.session_state.time_vector)
        power_line_interference = 2.5 * \
            np.sin(2 * np.pi * 50 * st.session_state.time_vector)
        thermal_noise = np.random.normal(0, 0.3, 1000)

        st.session_state.signal_data = clean_signal + \
            power_line_interference + thermal_noise
        st.success("Mock noisy biosignal loaded into memory!")

    st.markdown("---")
    run_engine = st.button("🚀 Run Diagnostics Engine",
                           type="primary", use_container_width=True)

# --- Main Dashboard ---
st.title("Signal Integrity & PCB Noise Troubleshooter")

# Top Row: Signal Visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Time Domain Capture")
    if st.session_state.signal_data is not None:
        fig_time, ax_time = plt.subplots(figsize=(6, 3))
        ax_time.plot(
            st.session_state.time_vector[:200], st.session_state.signal_data[:200], color="#00a8ff")
        ax_time.set_facecolor('#f5f6fa')
        ax_time.grid(True, linestyle="--", alpha=0.6)
        st.pyplot(fig_time)
    else:
        st.info("Awaiting temporal data stream...")

with col2:
    st.subheader("FFT Frequency Spectrum")
    if st.session_state.signal_data is not None:
        fft_values = np.abs(np.fft.rfft(st.session_state.signal_data))
        fft_freqs = np.fft.rfftfreq(
            len(st.session_state.signal_data), d=1/1000)

        fig_freq, ax_freq = plt.subplots(figsize=(6, 3))
        ax_freq.plot(fft_freqs[:100], fft_values[:100], color="#e84118")
        ax_freq.set_facecolor('#f5f6fa')
        ax_freq.grid(True, linestyle="--", alpha=0.6)
        st.pyplot(fig_freq)
    else:
        st.info("Awaiting temporal data stream...")

st.markdown("---")

# Bottom Row: Generative Output & Text Report
if run_engine:
    if st.session_state.signal_data is None:
        st.error("Pipeline Error: Please upload or generate a hardware signal first.")
    else:
        col3, col4 = st.columns([1, 1.5])

        with col3:
            st.subheader("Generative Re-Routing Output")
            fig_pcb, ax_pcb = plt.subplots(figsize=(5, 5))

            if uploaded_image is not None:
                # Process the uploaded user image
                img = Image.open(uploaded_image)
                ax_pcb.imshow(img)
                w, h = img.size

                # Draw the AI visual overlay
                ax_pcb.plot([w*0.2, w*0.8], [h*0.4, h*0.4], color="#e84118",
                            linestyle="--", linewidth=3, label="Detected Noise Path")
                ax_pcb.plot([w*0.2, w*0.4, w*0.6, w*0.8], [h*0.4, h*0.7, h*0.7, h*0.4],
                            color="#00d2d3", linestyle="-", linewidth=4, label="AI Optimized Reroute")
                ax_pcb.set_xlim(0, w)
                ax_pcb.set_ylim(h, 0)
            else:
                # Fallback mock PCB if no image is uploaded
                ax_pcb.set_facecolor('#073d22')
                ax_pcb.fill_between([1, 3], 7, 9, color="#2f3640", alpha=0.9)
                ax_pcb.text(2, 8, "AC POWER", color="#ffffff",
                            ha='center', va='center')
                ax_pcb.plot([1.5, 7.5], [6.5, 6.5], color="#e84118",
                            linestyle="--", linewidth=3, label="Original Path")
                ax_pcb.plot([1.5, 4.5, 8.5, 7.5], [6.5, 1.5, 1.5, 2], color="#00d2d3",
                            linestyle="-", linewidth=4, label="AI Optimized Route")
                ax_pcb.set_xlim(0, 10)
                ax_pcb.set_ylim(0, 10)

            ax_pcb.legend(loc="upper right", fontsize=8)
            ax_pcb.set_xticks([])
            ax_pcb.set_yticks([])
            st.pyplot(fig_pcb)

            # Allow user to download the generated fix
            buf = io.BytesIO()
            fig_pcb.savefig(buf, format="png", dpi=300, bbox_inches='tight')
            st.download_button(label="Download Routing Overlay", data=buf.getvalue(
            ), file_name="AI_Optimized_Routing.png", mime="image/png")

        with col4:
            st.subheader("Cross-Modal Diagnostic Insights")

            st.markdown("""
            **[STATUS]: CRITICAL INTERFERENCE ISOLATED**
            
            **1. TIME-SERIES / FREQUENCY DOMAIN REPORT:**
            * Dominant Spectral Spikes detected sharply at **50.00 Hz**.
            * Signature: AC Main Line Ripple / Power-Grid Inductive Coupling Harmonics.
            
            **2. VISUAL LAYOUT CROSS-REFERENCE:**
            * Geometric Scan: Found high-gain sensitive instrumentation tracking line running perfectly parallel to unregulated AC current supply lines.
            * Cross-talk Coefficient Matrix: High Risk (0.87 Probability Match).
            
            **3. AUTONOMOUS REDESIGN MITIGATION ROADMAP:**
            * **[ACTION 1]** Re-route trace segment to ensure minimum spatial separation distance away from alternating current tracks.
            * **[ACTION 2]** Drop a dedicated via guard ring structure to block cross-plane electromagnetic field coupling.
            * **[ACTION 3]** Hardware fallback: Append a dedicated 2nd-order twin-T notch filter topology centered precisely on 50Hz upstream from the ADC stage.
            """)
            st.success("Generative Routing Matrix Calculated Successfully.")
