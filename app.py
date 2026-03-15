import streamlit as st
import io
from src import parser, alignment, tree_builder, visualization

st.set_page_config(
    page_title="Penjelajah PhyloTree",
    layout="wide"
)

st.title("Penjelajah PhyloTree")
st.markdown(
    """
    Selamat datang di Penjelajah PhyloTree.
    Aplikasi ini memungkinkan Anda untuk membangun dan memvisualisasikan pohon filogenetik dari urutan DNA atau protein.
    Anda akan melihat bilah sisi untuk mengunggah urutan Anda dan mengonfigurasi analisis.
    Dua metode pembuatan pohon klasik diimplementasikan:
    1. **Neighbor-Joining (NJ)**: Metode berbasis jarak yang banyak digunakan karena kecepatan dan keakuratannya.
    2. **UPGMA**: Metode pengelompokan hierarkis yang didasarkan pada asumsi laju evolusi yang konstan.
    """
)

st.sidebar.header("1. Unggah Data")
uploaded_file = st.sidebar.file_uploader(
    "Unggah file FASTA",
    type=["fasta", "fa", "fas"]
)
use_sample = st.sidebar.checkbox(
    "Atau gunakan set data sampel yang disejajarkan",
    value=False
)

st.sidebar.header("2. Pengaturan")
distance_model = st.sidebar.selectbox(
    "Model Jarak",
    ["identity", "blosum62"],
    index=0
)
SAMPLE_FASTA = """>Human
ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAG
>Chimpanzee
ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAA
>Gorilla
ATGCGTACGTAGCTAGCTAGCTAGCTAGCGAG
>Orangutan
ATGCGTACGTAGCTAGCTAGCTAGCTAGCGGG
>Mouse
ATGCGTACGTAGCTAGCTAGCTAGCTAGTTTT
"""

fasta_data = None
if uploaded_file is not None:
    fasta_data = uploaded_file.getvalue().decode("utf-8")
elif use_sample:
    fasta_data = SAMPLE_FASTA

if fasta_data:
    try:
        st.header("Langkah 1: Validasi Penjajaran Urutan")
        records = parser.load_fasta(fasta_data)
        with st.expander("Lihat Urutan Mentah"):
            for rec in records:
                st.code(f">{rec.id}\n{rec.seq}")
            
            try:
                is_aligned, seq_length = parser.validate_alignment(records)
                st.success(f"Urutan disejajarkan pada panjang {seq_length} bp.")
                msa = parser.get_alignment(fasta_data)
            
            except ValueError as ve:
                st.warning(str(ve))
                st.info("Pohon berbasis jarak membutuhkan Penjajaran Urutan Berganda (MSA) terlebih dahulu.")

                if st.button("Sejajarkan Urutan dengan MUSCLE"):
                    with st.spinner("Menyejajarkan urutan..."):
                        try:
                            msa = alignment.prepare_alignment(records)
                            st.success("Penjajaran selesai!")
                            is_aligned = True
                        except Exception as e:
                            st.error(f"Penjajaran gagal: {e}")
                            st.stop()
                else:
                    st.stop()
            
            if 'msa' in locals() and msa:
                st.divider()
                st.header("Langkah 2: Matriks Jarak")
                st.markdown(
                    """
                    Matriks jarak mengkuantifikasi divergensi evolusioner antara setiap pasang urutan.
                    Sebelum membangun pohon, algoritma membandingkan setiap urutan dengan setiap urutan lainnya untuk menghitung **jarak genetik**.
                    Menggunakan model *identitas*, ini pada dasarnya adalah menghitung ketidakcocokan. Warna yang lebih gelap mewakili urutan yang lebih dekat kekerabatannya (jarak yang lebih kecil).
                    """
                )

                with st.spinner("Menghitung jarak..."):
                    dist_matrix = tree_builder.get_distance_matrix(msa, model=distance_model)
                    fig_matrix = visualization.plot_distance_matrix(dist_matrix)
                    st.pyplot(fig_matrix)

                    st.divider()
                    st.header("Langkah 3: Perbandingan Pohon")
                    st.markdown(
                        """
                        Sekarang, kita memasukkan Matriks Jarak yang sama persis itu ke dalam dua algoritma yang berbeda.
                        \n(Klik kanan pada gambar untuk melihat resolusi penuh)
                        """
                    )

                    trees = tree_builder.compare_trees(msa, model=distance_model)
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("UPGMA")
                        st.markdown("*Mengasumsikan jam molekuler yang konstan.*")
                        fig_upgma = visualization.plot_tree(trees['upgma'], title="UPGMA", type="rooted")
                        st.pyplot(fig_upgma)
                    
                    with col2:
                        st.subheader("Neighbor-Joining")
                        st.markdown("*Tidak ada asumsi jam molekuler.*")
                        fig_nj = visualization.plot_tree(trees['neighbor_joining'], title="Neighbor-Joining", type="unrooted")
                        st.pyplot(fig_nj)
    
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

else:
    st.info("👈 Silakan unggah file FASTA atau pilih set data sampel di bilah sisi untuk memulai.")