;;; Extensiones de Festival para Asterisk
;;; Archivo: /usr/share/festival/voices/spanish/festival.scm
;;; O en: /etc/festival.scm

;;; Este archivo define la función tts_textasterisk para generar
;;; contenido de TTS compatible con Asterisk.

;;; Define function to be called from Asterisk
(define (tts_textasterisk text mode)
  "Genera síntesis de voz compatible con Asterisk.
   
   Parámetros:
   - text: Texto a sintetizar
   - mode: Modo de procesamiento (opcional)
   
   Retorna: Utterancia sintetizada
   "
  (let ((utt (Utterance Text text)))
    ;; Aplicar procesamiento
    (utt.synth utt)
    ;; Retornar utterancia
    utt))

;;; Cargar soporte para español si está disponible
(cond
  ((file-exists? "/usr/share/festival/voices/spanish")
   (begin
     (require 'voice/spanish)
     (format t "Voz española cargada~%")))
  ((file-exists? "/usr/share/festival/lib/spanish.scm")
   (begin
     (load "/usr/share/festival/lib/spanish.scm")
     (format t "Español configurado~%")))
  (else
   (format t "Advertencia: Soporte para español no encontrado~%")))

;;; Configuración de parámetros para Asterisk
(set! *duration_stretch* 1.0)  ; Sin estiramiento de duración
(set! *ff_dur_stats* nil)       ; Sin estadísticas de duración

;;; Define voz por defecto
(if (boundp 'voice_el_male_bd)
    (voice_el_male_bd)
    (if (boundp 'voice_cmu_us_slt_cg)
        (voice_cmu_us_slt_cg)
        (Voice.default)))

;;; Funciones auxiliares para Asterisk

(define (festival_say_number number)
  "Convierte número a palabras habladas"
  (let ((utt (Utterance Text (number->words number))))
    (utt.synth utt)
    utt))

(define (festival_say_date date_string)
  "Convierte fecha a formato hablado"
  (let ((utt (Utterance Text (date->words date_string))))
    (utt.synth utt)
    utt))

(define (festival_say_time time_string)
  "Convierte hora a formato hablado"
  (let ((utt (Utterance Text (time->words time_string))))
    (utt.synth utt)
    utt))

;;; Funciones de convertir números/fechas a palabras
(define (number->words num)
  "Convierte número a palabras"
  (cond
    ((< num 0) (string-append "menos " (number->words (- num))))
    ((< num 10) 
     (elt '("cero" "uno" "dos" "tres" "cuatro" 
            "cinco" "seis" "siete" "ocho" "nueve") num))
    ((< num 20)
     (elt '("" "" "diez" "once" "doce" "trece" "catorce"
            "quince" "dieciséis" "diecisiete" "dieciocho" "diecinueve") num))
    ((< num 100)
     (let ((tens (/ num 10))
           (ones (mod num 10)))
       (cond
         ((= ones 0)
          (elt '("" "" "veinte" "treinta" "cuarenta" "cincuenta"
                 "sesenta" "setenta" "ochenta" "noventa") tens))
         (else
          (string-append 
            (elt '("" "" "veinte" "treinta" "cuarenta" "cincuenta"
                   "sesenta" "setenta" "ochenta" "noventa") tens)
            " " (number->words ones))))))
    (else (format nil "~D" num))))

(define (date->words date_string)
  "Convierte fecha a palabras: YYYY-MM-DD → texto"
  (if (string-match date_string "[0-9]+-[0-9]+-[0-9]+")
      (let* ((parts (string-split date_string "-"))
             (year (car parts))
             (month (cadr parts))
             (day (caddr parts)))
        (string-append day " de " (month->name month) " del " year))
      date_string))

(define (time->words time_string)
  "Convierte hora a palabras: HH:MM → texto"
  (if (string-match time_string "[0-9]+:[0-9]+")
      (let* ((parts (string-split time_string ":"))
             (hours (car parts))
             (mins (cadr parts)))
        (string-append "Las " hours " horas " mins " minutos"))
      time_string))

(define (month->name month_num)
  "Convierte número de mes a nombre"
  (elt '("" "enero" "febrero" "marzo" "abril" "mayo" "junio"
         "julio" "agosto" "septiembre" "octubre" "noviembre" "diciembre")
       (string->number month_num)))

;;; Verificación de instalación
(format t "Festival TTS extensiones para Asterisk cargadas~%")
(format t "Funciones disponibles:~%")
(format t "  - tts_textasterisk(text, mode)~%")
(format t "  - festival_say_number(num)~%")
(format t "  - festival_say_date(YYYY-MM-DD)~%")
(format t "  - festival_say_time(HH:MM)~%")
