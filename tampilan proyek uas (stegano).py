# PROGRAM   : Steganografi LSB
# ANGGOTA   : - Ria Azahra (2110106)
#             - Silmi Nur Jannah (2100376)
#             - Syifa Fatmawati (2103840)



from tkinter import filedialog
from PIL import Image
from cv2 import imread, imwrite  # untuk melakukan pengolahan citra dinamis secara real-time
import numpy as np  # untuk melakukan operasi vektor dan matriks dengan mengolah array dan array multidimensi
from base64 import urlsafe_b64encode  # menyembunyikan data penting, misalnya menyembunyikan string, password
from hashlib import md5  # untuk membuat hash string
from cryptography.fernet import Fernet  # untuk enkripsi dan dekripsi data


# GUI Python
import customtkinter as ctk                       
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Steganografi LSB (Ria Azahra, Silmi Nur Jannah, Syifa Fatmawati)")
app.geometry("1100x600")

# Upload Gambar (Cover Image)
def open_cover_image():
    global input_filepath
    input_filepath = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )

    if input_filepath:
        with open(input_filepath, 'r') as file:
            original_image = Image.open(input_filepath)
            image = original_image.copy()
        ratio = min(250 / image.width, 250 / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
        photo_image = ctk.CTkImage(light_image=image, dark_image=image, size=new_size)
        
        # Membuat Label untuk menampilkan gambar
        image_label = ctk.CTkLabel(app.tabview.tab("Embedding"), image=photo_image, text='')
        image_label.image = photo_image  # Menyimpan referensi ke objek gambar
        image_label.grid(row=1, column=0, padx=(50, 50), pady=(5, 5))
        
# Upload Gambar (Stego Image)
def open_stego_image():
    global stego_filepath
    stego_filepath = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )

    if stego_filepath:
        with open(stego_filepath, 'r') as file:
            original_image = Image.open(stego_filepath)
            image = original_image.copy()
        ratio = min(250 / image.width, 250 / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
        photo_image = ctk.CTkImage(light_image=image, dark_image=image, size=new_size)
        
        # Membuat Label untuk menampilkan gambar
        image_label = ctk.CTkLabel(app.tabview.tab("Ekstraksi"), image=photo_image, text='')
        image_label.image = photo_image  # Menyimpan referensi ke objek gambar
        image_label.grid(row=1, column=0, columnspan=2, padx=(50, 50), pady=(5, 5), sticky="ew")

        

# Download Stego-Image
def download_image():
    output_filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", ".png")]
    )
    if output_filepath:
        imwrite(output_filepath, stego_image)


# Mengembalikan representasi biner dari string
def str2bin(string):
    return ''.join((bin(ord(i))[2:]).zfill(7) for i in string)

# Mengembalikan representasi teks dari string biner
def bin2str(string):
    return ''.join(chr(int(string[i:i+7], 2)) for i in range(len(string))[::7])

# Enkripsi & Dekripsi (Cipher), Hashing MD5
def encrypt_decrypt(string, kunci, mode='enc'):
    _hash = md5(kunci.encode()).hexdigest()
    cipher_key = urlsafe_b64encode(_hash.encode())
    cipher = Fernet(cipher_key)
    if mode == 'enc':
        return cipher.encrypt(string.encode()).decode()
    else:
        return cipher.decrypt(string.encode()).decode()

# Embedding
def embed(input_filepath, plainteks, kunci=None, progressBar=None):
    if kunci is not None:
        data = encrypt_decrypt(plainteks, kunci, 'enc')
    else:
        data = plainteks
    data_length = bin(len(data))[2:].zfill(32)
    bin_data = iter(data_length + str2bin(data))
    img = imread(input_filepath, 1)
    height, width = img.shape[0], img.shape[1]
    encoding_capacity = height * width * 3
    total_bits = 32 + len(data) * 7
    if total_bits > encoding_capacity:
        app.stego_image_label = ctk.CTkLabel(app.tabview.tab("Embedding"), text="Data yang dipakai terlalu besar pada gambar ini!")
        app.stego_image_label.grid(row=1, column=0, padx=(50,50), pady=(10,5), sticky="nsew")
    completed = False
    modified_bits = 0
    progress = 0
    progress_fraction = 1 / total_bits

    for i in range(height):
        for j in range(width):
            pixel = img[i, j]
            for k in range(3):
                try:
                    x = next(bin_data)
                except StopIteration:
                    completed = True
                    break
                if x == '0' and pixel[k] % 2 == 1:
                    pixel[k] -= 1
                    modified_bits += 1
                elif x == '1' and pixel[k] % 2 == 0:
                    pixel[k] += 1
                    modified_bits += 1
                if progressBar is not None:  # jika progress bar object sudah selesai
                    progress += progress_fraction
                    progressBar.setValue(progress * 100)
            if completed:
                break
        if completed:
            break

    global stego_image
    stego_image = img

    original_image = Image.fromarray(img)
    ratio = min(250 /width, 250 /height)
    new_size = (int(width * ratio), int(height * ratio))
    image = original_image.resize(new_size, Image.LANCZOS)
    photo_image = ctk.CTkImage(image)

    # Membuat Label untuk menampilkan stego-image
    image_label = ctk.CTkLabel(app.tabview.tab("Embedding"), image=photo_image, text='')
    image_label.image = photo_image  # Menyimpan referensi ke objek gambar
    image_label.grid(row=1, column=1, padx=(50, 50), pady=(5, 5), sticky="ew")

    
hasil =''
# Ekstraksi
def ekstrak(stego_filepath, kunci=None, progressBar=None):
    global hasil
    result, extracted_bits, completed, number_of_bits = '', 0, False, None
    img = imread(stego_filepath)
    height, width = img.shape[0], img.shape[1]
    for i in range(height):
        for j in range(width):
            for k in img[i, j]:
                result += str(k % 2)
                extracted_bits += 1
                if progressBar is not None and number_of_bits is not None:
                    progressBar.setValue(100 * (extracted_bits / number_of_bits))
                if extracted_bits == 32 and number_of_bits is None:
                    number_of_bits = int(result, 2) * 7
                    result = ''
                    extracted_bits = 0
                elif extracted_bits == number_of_bits:
                    completed = True
                    break
            if completed:
                break
        if completed:
            break
    if kunci is None:
        hasil = bin2str(result)
    else:
        try:
            hasil = encrypt_decrypt(bin2str(result), kunci, 'dec')
        except:
            hasil = ("Password yang anda masukkan salah, silahkan coba lagi!")
    update_hasil_ekstrak()

def update_hasil_ekstrak():
    app.hasil_ekstrak.delete('1.0', ctk.END)
    app.hasil_ekstrak.insert(ctk.END, hasil)

#=============================================================================================================
# PROGRAM UTAMA

# configure grid layout (4x4)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0), weight=1)

# Identitas Kelompok
app.sidebar_frame = ctk.CTkFrame(app, width=200, corner_radius=0)
app.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
app.ria_label = ctk.CTkLabel(app.sidebar_frame, text="2110106 - Ria Azahra           ", font=ctk.CTkFont(size=15, weight="bold"))
app.ria_label.grid(row=0, column=0, padx=20, pady=(20, 1))
app.silmi_label = ctk.CTkLabel(app.sidebar_frame, text="2100376 - Silmi Nur Jannah", font=ctk.CTkFont(size=15, weight="bold"))
app.silmi_label.grid(row=1, column=0, padx=20, pady=(1, 1))
app.syifa_label = ctk.CTkLabel(app.sidebar_frame, text="2103840 - Syifa Fatmawati ", font=ctk.CTkFont(size=15, weight="bold"))
app.syifa_label.grid(row=2, column=0, padx=20, pady=(1, 1))

# Tab Menu
app.tabview = ctk.CTkTabview(app, width=500)
app.tabview.grid(row=0, column=1, padx=(20,20), pady=(10,20), sticky="nsew")
app.tabview.add("Embedding")
app.tabview.tab("Embedding").grid_columnconfigure(0, weight=1)
app.tabview.tab("Embedding").grid_columnconfigure(1, weight=1)
app.tabview.add("Ekstraksi")
app.tabview.tab("Ekstraksi").grid_columnconfigure((0,1), weight=1)

#------------------------------------ Embedding ------------------------------------
app.cover_image_label = ctk.CTkLabel(app.tabview.tab("Embedding"), text='Gambar yang akan disisipi pesan')
app.cover_image_label.grid(row=0, column=0, padx=(50,50), pady=(10,5), sticky="ew")
app.stego_image_label = ctk.CTkLabel(app.tabview.tab("Embedding"), text='Gambar yang sudah disisipi pesan')
app.stego_image_label.grid(row=0, column=1, padx=(50,50), pady=(10,5), sticky="ew")

app.pilih_gambar_button = ctk.CTkButton(app.tabview.tab("Embedding"), text="Pilih Gambar", command=open_cover_image)
app.pilih_gambar_button.grid(row=2, column=0, padx=(100,100), pady=(10,10), sticky="ew")
app.unduh_gambar_button = ctk.CTkButton(app.tabview.tab("Embedding"), text="Unduh Gambar", command=download_image)
app.unduh_gambar_button.grid(row=2, column=1, padx=(100,100), pady=(10,10), sticky="ew")

# INPUT
app.label_plain = ctk.CTkLabel(app.tabview.tab("Embedding"), text='Teks       : ', font=("montserrat",12))       
app.label_plain.grid(row=3, column=0, padx=(50,0), pady=(20,10), sticky="w")
app.plainteks = ctk.CTkEntry(app.tabview.tab("Embedding"), placeholder_text="Masukkan teks", width=650)
app.plainteks.grid(row=3, column=0, columnspan=2, padx=(0,50), pady=(20,10), sticky="e")

app.label_kunci = ctk.CTkLabel(app.tabview.tab("Embedding"), text='Kunci      : ', font=("montserrat",12))       
app.label_kunci.grid(row=4, column=0, padx=(50,0), pady=(5,10), sticky="w")
app.kunci = ctk.CTkEntry(app.tabview.tab("Embedding"), placeholder_text="Masukkan kunci", width=650)
app.kunci.grid(row=4, column=0, columnspan=2, padx=(0,50), pady=(5,10), sticky="e")

# EMBED
app.embed_button = ctk.CTkButton(app.tabview.tab("Embedding"), text="Embed", command=lambda: embed(input_filepath, app.plainteks.get(), app.kunci.get()))
app.embed_button.grid(row=5, column=0, columnspan=2, padx=(350,350), pady=(10,10), sticky="ew")

#------------------------------------ Ekstraksi ------------------------------------
# INPUT
app.stego_image_label = ctk.CTkLabel(app.tabview.tab("Ekstraksi"), text='Gambar yang telah disisipi pesan :')
app.stego_image_label.grid(row=0, column=0, padx=(50,50), pady=(20,10), sticky="ew")

app.unggah_stego_button = ctk.CTkButton(app.tabview.tab("Ekstraksi"), text="Unggah Stego Image", command=open_stego_image)
app.unggah_stego_button.grid(row=0, column=1, padx=(100,100), pady=(20,10), sticky="ew")

app.label_kunci = ctk.CTkLabel(app.tabview.tab("Ekstraksi"), text='Kunci      : ', font=("montserrat",12))       
app.label_kunci.grid(row=2, column=0, padx=(50,0), pady=(10,10), sticky="w")
app.kunci = ctk.CTkEntry(app.tabview.tab("Ekstraksi"), placeholder_text="Masukkan kunci", width=650)
app.kunci.grid(row=2, column=0, columnspan=2, padx=(0,50), pady=(5,10), sticky="e")

# EKSTRAK
app.ekstrak_button = ctk.CTkButton(app.tabview.tab("Ekstraksi"), text="Ekstraksi", command=lambda: ekstrak(stego_filepath, app.kunci.get()))
app.ekstrak_button.grid(row=3, column=0, columnspan=2, padx=(350,350), pady=(10,5), sticky="ew")

# OUTPUT
app.label_plain = ctk.CTkLabel(app.tabview.tab("Ekstraksi"), text='Teks       : ', font=("montserrat",12))       
app.label_plain.grid(row=4, column=0, padx=(50,0), pady=(10,0), sticky="w")
app.hasil_ekstrak = ctk.CTkTextbox(app.tabview.tab("Ekstraksi"),  width=650, height=200)
app.hasil_ekstrak.grid(row=5, column=0, columnspan=2, padx=(50,50), pady=(0,20), sticky="ew")
app.hasil_ekstrak.insert('0.0', hasil)



# Label untuk menampilkan gambar
label = ctk.CTkLabel(app, text="")



app.mainloop() 


