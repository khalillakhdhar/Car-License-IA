import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Changez ce chemin selon votre système

def extract_plate(img):
    # Convertissez l'image en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Appliquez un flou et un seuillage pour tenter de mettre en évidence le texte
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Utilisez Tesseract OCR pour extraire le texte
    text = pytesseract.image_to_string(thresh, config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return text

# Initialisez la capture vidéo à partir de la première caméra connectée
cap = cv2.VideoCapture(0)

while True:
    # Capturez un seul cadre de la vidéo
    ret, frame = cap.read()
    
    # Si le cadre est lu correctement ret est True
    if not ret:
        print("Impossible de recevoir le cadre (stream vidéo terminé?). Sortie...")
        break

    # Essayez d'extraire le numéro de plaque de l'image capturée
    plate_number = extract_plate(frame)
    print("Numéro de plaque détecté:", plate_number)

    # Affichez l'image capturée
    cv2.imshow('frame', frame)

    # Arrêtez le programme quand l'utilisateur appuie sur 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Quand tout est fait, relâchez la capture
cap.release()
cv2.destroyAllWindows()
