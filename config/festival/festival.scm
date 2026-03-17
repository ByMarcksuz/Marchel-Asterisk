;;; Configuración de Festival para Asterisk
;;; Archivo: /etc/festival.scm

;;; Establecer voz por defecto en español
;;; El idioma español debe estar instalado: festival-lang-spanish

(define (tts_textasterisk text mode)
  "Función para generar TTS compatible con Asterisk"
  (let ((utt (Utterance Text text)))
    (utt.synth utt)
    utt))

;;; Cargar voces disponibles
(if (file-exists? "/usr/share/festival/voices/spanish")
    (begin
      (require 'voice/spanish)
      ;; Usar voz española por defecto si está disponible
      (if (boundp 'voice_el_male_bd)
          (voice_el_male_bd)
          (Voice.default)))
    (begin
      ;; Si no hay español, usar voz por defecto (inglés)
      (print "Advertencia: Voz española no disponible")
      (Voice.default)))

;;; Configuración de parámetros de síntesis
(set! *duration_stretch* 1.0)
(set! *duration_model* t)
(set! *tts_window_size* 512)

;;; Configuración de calidad de audio
;;; Para Asterisk se recomienda 8kHz 16-bit mono
(set! *output-format* 'wav)

;;; Permitir conexión remota al servidor Festival
;;; El puerto por defecto es 1314
(set! *festival-port* 1314)
(set! *festival-listen-host* "localhost")

;;; Archivos de configuración adicionales
;;; Descomentar según sea necesario:

;;; Para usar voces presintetizadas en caché
;;; (load "/etc/festival/cache.scm")

;;; Para configuración de prosodias personalizadas
;;; (load "/etc/festival/prosodias.scm")

;;; Función auxiliar para verificar instalación
(defun check_festival_setup ()
  "Verifica que Festival esté correctamente configurado"
  (format t "Festival TTS Server~%")
  (format t "Versión: ~a~%" (car (split festival-version " ")))
  (format t "Puerto: ~a~%" *festival-port*)
  (format t "Host: ~a~%" *festival-listen-host*)
  (if (boundp 'current_voice)
      (format t "Voz actual: ~a~%" current_voice)))

;;; Ejecutar verificación al iniciar
(check_festival_setup)
