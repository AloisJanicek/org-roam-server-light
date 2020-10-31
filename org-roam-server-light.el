;;; org-roam-server-light.el --- External Org Roam server -*- lexical-binding: t; -*-

;; Author: Göktuğ Karakaşlı <karakasligk@gmail.com>
;;      Alois Janíček <janicek.dev@gmail.com>
;; URL: https://github.com/AloisJanicek/org-roam-server-light
;; Version: 0.1
;; Package-Requires: ((org-roam "1.2.1") (org "9.3") (emacs "26.1") (dash "2.17.0") (f "0.20.0"))

;; MIT License

;; Permission is hereby granted, free of charge, to any person obtaining a copy
;; of this software and associated documentation files (the "Software"), to deal
;; in the Software without restriction, including without limitation the rights
;; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
;; copies of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:

;; The above copyright notice and this permission notice shall be included in all
;; copies or substantial portions of the Software.

;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
;; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
;; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
;; SOFTWARE.

;;; Commentary:
;; A web application and web server to visualize the org-roam database.
;; Use M-x org-roam-server-light-mode RET to enable the global mode.
;; It will start a web server on http://127.0.0.1:8080
;;
;; This package differs from https://github.com/org-roam/org-roam-server by implementing
;; entire web server functionality in external python process as python seems to perform better
;; when building and serving JSON data for large and complex networks
;; like this: https://i.imgur.com/1D1VVoj.png


(require 'f)
(require 'org-roam)

;;; Code:
(defgroup org-roam-server-light nil
  "org-roam-server-light customizable variables."
  :group 'org-roam)

(defcustom org-roam-server-light-dir nil
  "Directory contenting org-roam-server-light repository."
  :group 'org-roam-server-light
  :type 'string)

(defcustom org-roam-server-light-network-vis-options nil
  "Options to be passed directly to vis.Network, in JSON format.
e.g. (json-encode (list (cons 'physics (list (cons 'enabled json-false)))))
or { \"physics\": { \"enabled\": false } }"
  :group 'org-roam-server-light
  :type 'string)

(defcustom org-roam-server-light-default-include-filters "null"
  "Options to set default include filters, in JSON format.
e.g. (json-encode (list (list (cons 'id \"test\") (cons 'parent \"tags\"))))
or [{ \"id\": \"test\", \"parent\" : \"tags\"  }]"
  :group 'org-roam-server-light
  :type 'string)

(defcustom org-roam-server-light-default-exclude-filters "null"
  "Options to set default exclude filters, in JSON format.
e.g. (json-encode (list (list (cons 'id \"test\") (cons 'parent \"tags\"))))
or [{ \"id\": \"test\", \"parent\" : \"tags\"  }]"
  :group 'org-roam-server-light
  :type 'string)

(defcustom org-roam-server-light-style nil
  "The CSS that can be used to customize the application."
  :group 'org-roam-server-light
  :type 'string)

(defcustom org-roam-server-light-tmp-dir
  (let ((dir-name "org-roam-server-light/"))
    (if (or IS-WINDOWS IS-MAC)
        (concat (replace-regexp-in-string "\\\\" "/"
                                          (or (getenv "TMPDIR")
                                              (getenv "TMP")))
                "/" dir-name)
      (concat "/tmp/" dir-name)))
  "Directory contenting org-roam-server-light repository."
  :group 'org-roam-server-light
  :type 'string)

(defvar org-roam-server-light-last-roam-buffer nil
  "Variable storing name of the last org-roam buffer.")

(defun org-roam-server-light-update-last-buffer ()
  "Update `org-roam-server-light-last-roam-buffer'."
  (let ((buf (or (buffer-base-buffer (current-buffer)) (current-buffer))))
    (when (org-roam--org-roam-file-p
           (buffer-file-name buf))
      (setq org-roam-server-light-last-roam-buffer
            (car (last (split-string (org-roam--path-to-slug (buffer-name buf)) "/"))))
      (f-write-text
       org-roam-server-light-last-roam-buffer
       'utf-8
       (concat org-roam-server-light-tmp-dir "org-roam-server-light-last-roam-buffer")))))

(defun org-roam-server-light-find-file-hook-function ()
  "If the current visited file is an `org-roam` file, update the current buffer."
  (when (org-roam--org-roam-file-p)
    (add-hook 'post-command-hook #'org-roam-server-light-update-last-buffer nil t)
    (org-roam-server-light-update-last-buffer)))

;;;###autoload
(define-minor-mode org-roam-server-light-mode
  "Start the http server and serve org-roam files."
  :lighter ""
  :global t
  :init-value nil
  (let* ((title "org-roam-server-light"))
    (if (not (ignore-errors org-roam-server-light-mode))
        (progn
          (when (get-process title)
            (delete-process title))
          (remove-hook 'find-file-hook #'org-roam-server-light-find-file-hook-function nil)
          (dolist (buf (org-roam--get-roam-buffers))
            (with-current-buffer buf
              (remove-hook 'post-command-hook #'org-roam-server-light-update-last-buffer t))))
      (progn
        (add-hook 'find-file-hook #'org-roam-server-light-find-file-hook-function nil nil)
        (unless (file-exists-p org-roam-server-light-tmp-dir)
          (make-directory org-roam-server-light-tmp-dir))
        (f-write-text org-roam-server-light-network-vis-options
                      'utf-8
                      (expand-file-name "org-roam-server-light-network-vis-options" org-roam-server-light-tmp-dir))
        (f-write-text org-roam-server-light-default-include-filters
                      'utf-8
                      (expand-file-name "org-roam-server-light-default-include-filters" org-roam-server-light-tmp-dir))
        (f-write-text org-roam-server-light-default-exclude-filters
                      'utf-8
                      (expand-file-name "org-roam-server-light-default-exclude-filters" org-roam-server-light-tmp-dir))
        (f-write-text org-roam-server-light-style
                      'utf-8
                      (expand-file-name "org-roam-server-light-style" org-roam-server-light-tmp-dir))
        (f-write-text org-roam-db-location
                      'utf-8
                      (expand-file-name "org-roam-db-location" org-roam-server-light-tmp-dir))
        (f-write-text org-roam-directory
                      'utf-8
                      (expand-file-name "org-roam-directory" org-roam-server-light-tmp-dir))
        (let ((default-directory org-roam-server-light-dir))
          (start-process-shell-command "org-roam-server-light" "org-roam-server-light-output-buffer" "python main.py"))))))


(provide 'org-roam-server-light)
;;; org-roam-server-light.el ends here
