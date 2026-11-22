import turtle
import chess

# Ekran ve Sabit Ayarlar
KARE_BOYUTU = 60
BASLANGIC_X = -240
BASLANGIC_Y = 240

TAS_SEMBOLLERI = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
}

ekran = turtle.Screen()
ekran.title("Python Turtle Satranç")
ekran.setup(width=560, height=580)
ekran.tracer(0)  # Ekran titremesini önlemek için anlık çizimi kapat

kalem = turtle.Turtle()
kalem.hideturtle()
kalem.speed(0)

tahta = chess.Board()
secili_kare = None


def kare_koordinati_bul(satir, sutun):
    x = BASLANGIC_X + sutun * KARE_BOYUTU
    y = BASLANGIC_Y - satir * KARE_BOYUTU
    return x, y


def tahtayi_ciz():
    kalem.clear()
    
    # 1. Kareleri ve Seçili Kare Vurgusunu Çiz
    for satir in range(8):
        for sutun in range(8):
            x, y = kare_koordinati_bul(satir, sutun)
            kare_indeksi = chess.square(sutun, 7 - satir)
            
            if secili_kare == kare_indeksi:
                renk = "#f6f669"  # Seçili kare sarısı
            elif (satir + sutun) % 2 == 0:
                renk = "#eeeed2"  # Açık kare
            else:
                renk = "#769656"  # Koyu kare
                
            kalem.penup()
            kalem.goto(x, y)
            kalem.pendown()
            kalem.fillcolor(renk)
            kalem.begin_fill()
            for _ in range(4):
                kalem.forward(KARE_BOYUTU)
                kalem.right(90)
            kalem.end_fill()

    # 2. Taşları Çiz
    for kare_indeksi in chess.SQUARES:
        tas = tahta.piece_at(kare_indeksi)
        if tas:
            sutun = chess.square_file(kare_indeksi)
            satir = 7 - chess.square_rank(kare_indeksi)
            x, y = kare_koordinati_bul(satir, sutun)
            
            kalem.penup()
            kalem.goto(x + KARE_BOYUTU / 2, y - KARE_BOYUTU + 8)
            kalem.color("black")
            kalem.write(TAS_SEMBOLLERI[tas.symbol()], align="center", font=("Arial", 36, "normal"))

    # 3. Oyun Durumu Mesajı
    kalem.penup()
    kalem.goto(0, -270)
    kalem.color("black")
    if tahta.is_checkmate():
        kazanan = "Siyah" if tahta.turn == chess.WHITE else "Beyaz"
        durum = f"ŞAH MAT! Kazanan: {kazanan}"
    elif tahta.is_stalemate():
        durum = "PAT! Oyun Berabere"
    elif tahta.is_check():
        sira = "Beyaz" if tahta.turn == chess.WHITE else "Siyah"
        durum = f"ŞAH! Sıra: {sira}"
    else:
        sira = "Beyaz" if tahta.turn == chess.WHITE else "Siyah"
        durum = f"Sıra: {sira}"
        
    kalem.write(durum, align="center", font=("Arial", 14, "bold"))
    ekran.update()


def tiklama_isle(x, y):
    global secili_kare
    if tahta.is_game_over():
        return

    # Tıklanan koordinatı satır ve sütuna çevir
    sutun = int((x - BASLANGIC_X) // KARE_BOYUTU)
    satir = int((BASLANGIC_Y - y) // KARE_BOYUTU)

    if 0 <= satir < 8 and 0 <= sutun < 8:
        tiklanan_kare = chess.square(sutun, 7 - satir)
        
        if secili_kare is None:
            # İlk tıklama: Kendi taşını seç
            tas = tahta.piece_at(tiklanan_kare)
            if tas and tas.color == tahta.turn:
                secili_kare = tiklanan_kare
        else:
            # İkinci tıklama: Hamle yap veya başka taş seç
            hamle = chess.Move(secili_kare, tiklanan_kare)
            
            # Piyon terfisi kontrolü (otomatik vezir yapar)
            if chess.Move(secili_kare, tiklanan_kare, promotion=chess.QUEEN) in tahta.legal_moves:
                hamle = chess.Move(secili_kare, tiklanan_kare, promotion=chess.QUEEN)
                
            if hamle in tahta.legal_moves:
                tahta.push(hamle)
                secili_kare = None
            else:
                # Kendi başka taşına tıkladıysa seçimi değiştir
                tas = tahta.piece_at(tiklanan_kare)
                if tas and tas.color == tahta.turn:
                    secili_kare = tiklanan_kare
                else:
                    secili_kare = None
                    
        tahtayi_ciz()


# Oyunu Başlat
tahtayi_ciz()
ekran.onclick(tiklama_isle)
ekran.mainloop()
