"""
Auto Timestamp - Automated File Timestamp Modifier
Copyright (c) 2024-2025 Airbank1
https://github.com/Airbank1/auto-timestamp

Licensed under AGPL-3.0
Free to use and modify. If you share it, mention the source. Thanks!
"""

import os
import re
import time
import datetime
import ctypes
from ctypes import wintypes

# ===================================
# SECTION 1: CONFIGURATION & CONSTANTS
# ===================================

class Config:
    """Configuration globale du programme"""
    TERMINAL_WIDTH = 133
    BOX_WIDTH = 133
    MAX_FILENAME_LENGTH = 80
    LONG_FILENAME_MAX_LENGTH = 125
    PROGRESS_SLEEP_TIME = 0.1
    
    # Codes couleurs ANSI
    COLORS = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'blue_header': '\33[38;5;19m',
        'blue_manual': '\33[38;5;18m',
        'purple': '\033[35m',
        'error_red': '\033[38;5;124m',
        'reset': '\033[0m'
    }
    
    # ASCII Art Headers
    AUTO_HEADER = [
        " █████  ██    ██ ████████  ██████      ████████ ██ ███    ███ ███████ ███████ ████████  █████  ███    ███ ██████ ",
        "██   ██ ██    ██    ██    ██    ██        ██    ██ ████  ████ ██      ██         ██    ██   ██ ████  ████ ██   ██",
        "███████ ██    ██    ██    ██    ██        ██    ██ ██ ████ ██ █████   ███████    ██    ███████ ██ ████ ██ ██████ ",
        "██   ██ ██    ██    ██    ██    ██        ██    ██ ██  ██  ██ ██           ██    ██    ██   ██ ██  ██  ██ ██     ",
        "██   ██  ██████     ██     ██████         ██    ██ ██      ██ ███████ ███████    ██    ██   ██ ██      ██ ██     "
    ]
    
    MANUAL_HEADER = [
        "  ███    ███  █████  ███    ██ ██    ██  █████  ██       ████████ ██ ███    ███ ███████ ███████ ████████  █████  ███    ███ ██████ ",
        "  ████  ████ ██   ██ ████   ██ ██    ██ ██   ██ ██          ██    ██ ████  ████ ██      ██         ██    ██   ██ ████  ████ ██   ██",
        "  ██ ████ ██ ███████ ██ ██  ██ ██    ██ ███████ ██          ██    ██ ██ ████ ██ █████   ███████    ██    ███████ ██ ████ ██ ██████ ",
        "  ██  ██  ██ ██   ██ ██  ██ ██ ██    ██ ██   ██ ██          ██    ██ ██  ██  ██ ██           ██    ██    ██   ██ ██  ██  ██ ██     ",
        "  ██      ██ ██   ██ ██   ████  ██████  ██   ██ ███████     ██    ██ ██      ██ ███████ ███████    ██    ██   ██ ██      ██ ██     "
    ]

# ===================================
# SECTION 2: SYSTÈME & UTILITAIRES DE BASE
# ===================================

class SystemUtils:
    """Utilitaires système de bas niveau"""
    
    @staticmethod
    def clear_screen():
        """Efface l'écran de la console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def maximize_cmd():
        """Simule la pression de la touche Alt+Enter pour maximiser la fenêtre CMD"""
        ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)  # Press ALT
        ctypes.windll.user32.keybd_event(0x0D, 0, 0, 0)  # Press Enter
        ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)  # Relâche ALT
        ctypes.windll.user32.keybd_event(0x0D, 0, 2, 0)  # Relâche Enter

class FileSystemUtils:
    """Utilitaires pour les opérations sur les fichiers"""
    
    @staticmethod
    def get_files_in_directory(directory_path):
        """Obtient la liste des fichiers dans le répertoire, excluant le script actuel"""
        current_dir = directory_path
        files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
        files = [f for f in files if f not in [os.path.basename(__file__)]]
        return files
    
    @staticmethod
    def set_file_timestamp(filename, new_date):
        """Change les dates de création, modification, et accès"""
        timestamp = time.mktime(new_date.timetuple())
        
        # Modifier les dates d'accès et de modification
        os.utime(filename, (timestamp, timestamp))
        
        # Modifier la date de création sous Windows
        if os.name == 'nt':
            try:
                FILETIME_EPOCH = 116444736000000000
                HUNDREDS_OF_NANOSECONDS = 10000000
                timestamp_100ns = int(timestamp * HUNDREDS_OF_NANOSECONDS) + FILETIME_EPOCH
                ctime = wintypes.FILETIME(timestamp_100ns & 0xFFFFFFFF, timestamp_100ns >> 32)
                kernel32 = ctypes.windll.kernel32
                handle = kernel32.CreateFileW(filename, 256, 0, None, 3, 128, None)
                
                if handle != -1:
                    kernel32.SetFileTime(handle, ctypes.byref(ctime), ctypes.byref(ctime), ctypes.byref(ctime))
                    kernel32.CloseHandle(handle)
                    return True
                else:
                    return False
            except Exception:
                return False
        return True

# ===================================
# SECTION 3: PARSING & EXTRACTION DE DONNÉES
# ===================================

class DateTimeParser:
    """Gestionnaire pour l'extraction et le parsing des dates"""
    
    @staticmethod
    def extract_date_from_filename(filename):
        """Extrait la date du nom de fichier"""
        number_parts = re.findall(r'\d+', filename)
        
        date_part = None
        time_part = None
        
        for part in number_parts:
            if len(part) == 8 and part.isdigit():
                date_part = part
            elif len(part) == 6 and part.isdigit():
                time_part = part
        
        try:
            if date_part and time_part:
                return datetime.datetime.strptime(
                    f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]} {time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}", 
                    "%Y-%m-%d %H:%M:%S"
                )
        except ValueError:
            pass
        
        return None
    
    @staticmethod
    def parse_manual_datetime(input_str):
        """Parse une date et heure saisies manuellement avec les formats spécifiques"""
        try:
            input_str = input_str.strip()
            
            # Si vide, retourner None (annuler)
            if not input_str:
                return None
            
            today = datetime.datetime.now()
            
            # Format "24/08/2025 17:36"
            if len(input_str.split()) == 2:
                date_part, time_part = input_str.split()
                if '/' in date_part and ':' in time_part:
                    try:
                        date_obj = datetime.datetime.strptime(date_part, "%d/%m/%Y")
                        time_obj = datetime.datetime.strptime(time_part, "%H:%M").time()
                        return datetime.datetime.combine(date_obj.date(), time_obj)
                    except ValueError:
                        return None
            
            # Format "Hier à 20:29"
            if input_str.lower().startswith("hier à ") and ':' in input_str:
                time_part = input_str.lower().replace("hier à ", "")
                try:
                    time_obj = datetime.datetime.strptime(time_part, "%H:%M").time()
                    yesterday = today - datetime.timedelta(days=1)
                    return datetime.datetime.combine(yesterday.date(), time_obj)
                except ValueError:
                    return None
            
            # Format "20:29" (aujourd'hui)
            if ':' in input_str and len(input_str.split(':')) == 2:
                try:
                    time_obj = datetime.datetime.strptime(input_str, "%H:%M").time()
                    return datetime.datetime.combine(today.date(), time_obj)
                except ValueError:
                    return None
            
            return None
            
        except Exception:
            return None

# ===================================
# SECTION 4: FORMATAGE & AFFICHAGE DE TEXTE
# ===================================

class TextFormatter:
    """Utilitaires pour le formatage de texte et noms de fichiers"""
    
    @staticmethod
    def truncate_filename(filename, max_length=Config.MAX_FILENAME_LENGTH):
        """Tronque le nom de fichier à max_length caractères (strictement supérieur), ajoute '…' si besoin."""
        if len(filename) > max_length:
            return filename[:max_length-1] + "…"
        return filename
    
    @staticmethod
    def split_long_filename_lines(filename, max_length=Config.LONG_FILENAME_MAX_LENGTH):
        """Découpe un nom de fichier trop long en plusieurs lignes de max_length caractères, avec indentation pour les suivantes."""
        lines = []
        for i in range(0, len(filename), max_length):
            if i == 0:
                lines.append(filename[i:i+max_length])
            else:
                lines.append(filename[i:i+max_length])
        return lines
    
    @staticmethod
    def format_file_line_with_date(filename, date):
        """Formate une ligne de fichier avec sa date et son heure"""
        display_filename = TextFormatter.truncate_filename(filename)
        date_str = date.strftime("%Y-%m-%d")
        time_str = date.strftime("%H:%M:%S")
        info_text = f"  Date: {date_str}  Heure: {time_str} "
        current_length = len(display_filename) + 1 + len(info_text)
        remaining_length = 129 - current_length
        padding = "━ " * (remaining_length // 2)
        return f"{display_filename} {padding}{info_text}"

class HeaderRenderer:
    """Gestionnaire pour l'affichage des en-têtes"""
    
    @staticmethod
    def print_header():
        """Affiche l'en-tête du programme avec couleur bleue"""
        print()
        for line in Config.AUTO_HEADER:
            print(Config.COLORS['blue_header'] + 10*" " + line + Config.COLORS['reset'])
        print()
    
    @staticmethod
    def print_manual_header():
        """Affiche l'en-tête pour la modification manuelle"""
        print()
        for line in Config.MANUAL_HEADER:
            print(Config.COLORS['blue_manual'] + line + Config.COLORS['reset'])
        print()
    
    @staticmethod
    def print_separator():
        """Affiche une ligne de séparation"""
        print("─" * Config.TERMINAL_WIDTH)

# ===================================
# SECTION 5: INTERFACES & COMPOSANTS UI
# ===================================

class ProgressBarRenderer:
    """Gestionnaire de la barre de progression"""
    
    @staticmethod
    def print_progress_bar(current, total, filename=""):
        """Affiche une barre de progression sans scintillement"""
        if total == 0:
            return
        
        total_width = Config.TERMINAL_WIDTH - 1
        bar_length = total_width
        progress = current / total
        filled_length = int(bar_length * progress)
        
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percent = round(progress * 100, 1)
        
        # Format filename and percentage
        percentage_text = f"{percent:>5.1f}%"
        available_space = total_width - len(percentage_text)
        filename_space = available_space - 2  # Account for " | " separator
        truncated_filename = filename[:filename_space] if filename else ""
        
        # Save cursor position
        print("\033[s", end='')
        # Move cursor to start of line and print bar
        print(f"\r {bar}", end='', flush=True)
        # Restore cursor position and move down 1 line
        print(f"\033[u\033[B\r  {truncated_filename:<{filename_space}} {percentage_text}", end="", flush=True)
        # Move cursor back to saved position
        print("\033[u", end='', flush=True)

class BoxRenderer:
    """Gestionnaire pour l'affichage des boîtes colorées"""
    
    @staticmethod
    def _get_title_line(title):
        """Génère la ligne de titre centrée pour une boîte"""
        if title == "FICHIERS TRAITÉS":
            return f"{' ' * 57}FICHIERS TRAITÉS{' ' * 57}"
        elif title == "FICHIERS NON TRAITÉS":
            return f"{' ' * 55}FICHIERS NON TRAITÉS{' ' * 55}"
        elif title == "FICHIER TRAITÉ":
            return f"{' ' * 58}FICHIER TRAITÉ{' ' * 58}"
        elif title == "FICHIER NON TRAITÉ":
            return f"{' ' * 56}FICHIER NON TRAITÉ{' ' * 56}"
        else:
            # Fallback au centrage automatique pour autres titres
            title_padding = (Config.BOX_WIDTH - 4 - len(title)) // 2
            remaining_padding = Config.BOX_WIDTH - 4 - len(title) - title_padding
            return f"{' ' * title_padding}{title}{' ' * remaining_padding}"
    
    @staticmethod
    def _render_auto_content_line(line, title, color):
        """Rend une ligne de contenu pour le mode automatique avec gestion spéciale pour fichiers non traités"""
        colors = Config.COLORS
        reset = colors['reset']
        
        if title in ("FICHIERS NON TRAITÉS", "FICHIER NON TRAITÉ"):
            # Mode AUTO : garder les "—"
            prefix, filename = line.split(" — ", 1) if " — " in line else ("", line)
            split_lines = TextFormatter.split_long_filename_lines(filename)
            for idx, l in enumerate(split_lines):
                display = f" — {l}" if idx == 0 and prefix == "" else f"   {l}"
                content_padding = Config.BOX_WIDTH - 3 - len(display) - 1
                print(f" {colors[color]}│ {display}{' ' * content_padding}│{reset}")
        else:
            content_padding = Config.BOX_WIDTH - 3 - len(line) - 1
            print(f" {colors[color]}│ {line}{' ' * content_padding}│{reset}")
    
    @staticmethod
    def _render_manual_content_line(line, title, color):
        """Rend une ligne de contenu pour le mode manuel avec numérotation propre"""
        colors = Config.COLORS
        reset = colors['reset']
        
        if title in ("FICHIERS NON TRAITÉS", "FICHIER NON TRAITÉ"):
            parts = line.split('. ', 1)
            number_part = parts[0]
            filename = parts[1] if len(parts) > 1 else ""
            available_width = Config.BOX_WIDTH - 6 - len(number_part)
            remaining = filename
            first_line = True
            
            while remaining:
                if first_line:
                    chunk = remaining[:available_width]
                    display = f"{number_part}. {chunk}"
                    first_line = False
                else:
                    indent = " " * (len(number_part) + 2)
                    chunk = remaining[:Config.BOX_WIDTH - 4 - len(indent)]
                    display = f"{indent}{chunk}"
                
                content_padding = Config.BOX_WIDTH - 2 - len(display) - 1
                print(f" {colors[color]}│{display}{' ' * content_padding}│{reset}")
                remaining = remaining[len(chunk):]
        else:
            content_padding = Config.BOX_WIDTH - 3 - len(line) - 1
            print(f" {colors[color]}│ {line}{' ' * content_padding}│{reset}")
    
    @staticmethod
    def print_auto_box(title, color_code, content_lines):
        """Affiche un encadré coloré pour le mode automatique"""
        colors = Config.COLORS
        color = colors.get(color_code, colors['reset'])
        reset = colors['reset']
        
        print(f" {color}╭{'─' * 130}╮{reset}")
        
        # Ligne du titre
        title_line = BoxRenderer._get_title_line(title)
        print(f" {color}│{title_line}│{reset}")
        
        # Ligne de séparation si il y a du contenu
        if content_lines:
            print(f" {color}├{'─' * 130}┤{reset}")
        
        # Affichage du contenu mode AUTO
        for line in content_lines:
            BoxRenderer._render_auto_content_line(line, title, color_code)

        print(f" {color}╰{'─' * 130}╯{reset}")
    
    @staticmethod
    def print_manual_box(title, color_code, content_lines):
        """Affiche un encadré coloré pour le mode manuel"""
        colors = Config.COLORS
        color = colors.get(color_code, colors['reset'])
        reset = colors['reset']
        
        print(f" {color}╭{'─' * 130}╮{reset}")
        
        # Ligne du titre
        title_line = BoxRenderer._get_title_line(title)
        print(f" {color}│{title_line}│{reset}")
        
        # Ligne de séparation si il y a du contenu
        if content_lines:
            print(f" {color}├{'─' * 130}┤{reset}")
        
        # Affichage du contenu mode MANUEL
        for line in content_lines:
            BoxRenderer._render_manual_content_line(line, title, color_code)

        print(f" {color}╰{'─' * 130}╯{reset}")
    
    @staticmethod
    def print_mixed_box(title, content_lines_with_colors):
        """Affiche un encadré avec lignes de couleurs différentes (pour résumé final)"""
        colors = Config.COLORS
        reset = colors['reset']
        
        print(f" {colors['green']}╭{'─' * 130}╮{reset}")

        title_line = BoxRenderer._get_title_line(title)
        print(f" {colors['green']}│{title_line}│{reset}")
        
        # Ligne de séparation si il y a du contenu
        if content_lines_with_colors:
            print(f" {colors['green']}├{'─' * 130}┤{reset}")

        for line, color in content_lines_with_colors:
            # Pour les fichiers non traités du résumé final, garder les "—"
            if color == 'red' and (title == "FICHIERS NON TRAITÉS" or title == "FICHIER NON TRAITÉ"):
                prefix, filename = line.split(" — ", 1) if " — " in line else ("", line)
                split_lines = TextFormatter.split_long_filename_lines(filename)
                for idx, l in enumerate(split_lines):
                    display = f" — {l}" if idx == 0 and prefix == "" else f"   {l}"
                    content_padding = Config.BOX_WIDTH - 3 - len(display) - 1
                    print(f" {colors['green']}│{colors[color]} {display}{' ' * content_padding}{colors['green']}│{reset}")
            elif color == 'yellow':
                content_padding = Config.BOX_WIDTH - 4 - len(line) - 1
                print(f" {colors['green']}│ {colors['yellow']}{line}{colors['green']}{' ' * content_padding}│{reset}")
            else:
                content_padding = Config.BOX_WIDTH - 4 - len(line) - 1
                print(f" {colors[color]}│ {line}{' ' * content_padding}│{reset}")

        print(f" {colors['green']}╰{'─' * 130}╯{reset}")

# ===================================
# SECTION 6: LOGIQUE DE TRAITEMENT AUTOMATIQUE
# ===================================

class AutoProcessor:
    """Gestionnaire pour le traitement automatique des fichiers"""
    
    def __init__(self):
        self.processed_files = []
        self.unprocessed_files = []
    
    def process_file(self, filename):
        """Traite un fichier individual automatiquement"""
        new_date = DateTimeParser.extract_date_from_filename(filename)
        
        if new_date:
            if FileSystemUtils.set_file_timestamp(filename, new_date):
                self.processed_files.append((filename, new_date))
                return True
            else:
                self.unprocessed_files.append(filename)
                return False
        else:
            self.unprocessed_files.append(filename)
            return False
    
    def process_files_with_progress(self, files):
        """Traite une liste de fichiers avec affichage de la progression"""
        for i, file in enumerate(files):
            ProgressBarRenderer.print_progress_bar(i, len(files), file)
            self.process_file(file)
            time.sleep(Config.PROGRESS_SLEEP_TIME)  # Petite pause pour voir la progression
        
        # Finaliser la barre de progression
        ProgressBarRenderer.print_progress_bar(len(files), len(files), "Terminé!")
        print("\n")

# ===================================
# SECTION 7: LOGIQUE DE TRAITEMENT MANUEL
# ===================================

class ManualProcessor:
    """Gestionnaire pour le traitement manuel des fichiers"""
    
    def __init__(self):
        self.processed_files = []
    
    def parse_user_selection(self, choice, remaining_files):
        """Parse la sélection utilisateur et retourne le nom du fichier sélectionné"""
        choice = choice.strip()
        
        # 1. Nom exact du fichier (priorité absolue)
        if choice in remaining_files:
            return choice
        
        # 2. Si ligne copiée avec │, extraire juste le numéro après │
        if '│' in choice:
            number_match = re.search(r'│\s*(\d+)\.', choice)
            if number_match:
                try:
                    file_index = int(number_match.group(1)) - 1
                    if 0 <= file_index < len(remaining_files):
                        return remaining_files[file_index]
                except (ValueError, IndexError):
                    pass
        
        # 3. Si c'est un numéro pur (avec ou sans point)
        try:
            if choice.isdigit() or (choice.endswith('.') and choice[:-1].isdigit()):
                file_index = int(choice.rstrip('.')) - 1
                if 0 <= file_index < len(remaining_files):
                    return remaining_files[file_index]
        except (ValueError, IndexError):
            pass
        
        # 4. Chercher un numéro dans la chaîne
        number_match = re.search(r'(\d+)\.', choice)
        if number_match:
            try:
                file_index = int(number_match.group(1)) - 1
                if 0 <= file_index < len(remaining_files):
                    return remaining_files[file_index]
            except (ValueError, IndexError):
                pass
        
        return None
    
    def calculate_input_lines_used(self, choice):
        """Calcule le nombre de lignes utilisées par l'input utilisateur"""
        input_text = f"  Votre choix : {choice}"
        terminal_width = Config.TERMINAL_WIDTH
        return (len(input_text) + terminal_width - 1) // terminal_width
    
    def clear_input_lines(self, lines_count):
        """Efface les lignes d'input de la console"""
        for _ in range(lines_count):
            print("\033[A\033[2K\r", end="")  # Remonte d'une ligne et l'efface
    
    def process_file_manually(self, filename):
        """Traite un fichier manuellement avec saisie utilisateur"""
        print()
        filename_line = f"Modification du fichier : {filename}"
        print(filename_line)
        HeaderRenderer.print_separator()
        
        # Demander la date/heure directement
        datetime_input = input("Entrez la date et l'heure : ").strip()
        
        # Parser la date et l'heure
        new_datetime = DateTimeParser.parse_manual_datetime(datetime_input)
        
        if new_datetime:
            # Appliquer la modification sans confirmation
            if FileSystemUtils.set_file_timestamp(filename, new_datetime):
                self.processed_files.append((filename, new_datetime))
                date_formatted = new_datetime.strftime('%d/%m/%Y %H:%M:%S')
                print(f"\033[A\033[2K\rFichier modifié avec succès : {Config.COLORS['purple']}{date_formatted}{Config.COLORS['reset']}")
                return True
            else:
                print(f"\033[A\033[2K\r{Config.COLORS['error_red']}Erreur lors de la modification du fichier{Config.COLORS['reset']}")
                return False
        elif datetime_input == "":
            print("\033[A\033[2K\rModification annulée")
            return False
        else:
            print(f"\033[A\033[2K\r{Config.COLORS['error_red']}Format invalide{Config.COLORS['reset']}")
            return False
    
    def manual_timestamp_modification(self, unprocessed_files):
        """Interface pour modifier manuellement les timestamps"""
        if not unprocessed_files:
            return [], []
        
        remaining_unprocessed = list(unprocessed_files)
        
        while True:
            SystemUtils.clear_screen()
            HeaderRenderer.print_manual_header()
            HeaderRenderer.print_separator()
            if len(remaining_unprocessed) == 1:
                print("  Fichier restant à traiter :")
            else:
                print("  Fichiers restants à traiter :")
            
            # Afficher le tableau rouge des fichiers non traités (MODE MANUEL)
            if remaining_unprocessed:
                title = "FICHIER NON TRAITÉ" if len(remaining_unprocessed) == 1 else "FICHIERS NON TRAITÉS"
                
                # Calculer la largeur maximale des numéros
                max_num = len(remaining_unprocessed)
                max_num_width = len(str(max_num))  # Largeur du plus grand numéro
                
                # Créer les lignes avec espacement ajusté
                unprocessed_lines = []
                for i, filename in enumerate(remaining_unprocessed):
                    current_num = i + 1
                    current_num_width = len(str(current_num))
                    # FORMULE CORRECTE : 2 espaces pour le plus grand + différence de longueur
                    spaces_needed = 2 + (max_num_width - current_num_width)
                    spaces = " " * spaces_needed
                    formatted_line = f"{spaces}{current_num}. {filename}"
                    unprocessed_lines.append(formatted_line)
                
                BoxRenderer.print_manual_box(title, "red", unprocessed_lines)
                
                choice = input(" Votre choix : ").strip()
                
                # Si l'utilisateur appuie directement sur Entrée, quitter
                if not choice:
                    break
                
                selected_filename = self.parse_user_selection(choice, remaining_unprocessed)
                
                if selected_filename:
                    # Calculer le nombre de lignes prises par l'input
                    lines_used = self.calculate_input_lines_used(choice)
                    # Effacer toutes les lignes utilisées par l'input
                    self.clear_input_lines(lines_used)
                    
                    # Traitement du fichier sélectionné
                    success = self.process_file_manually(selected_filename)
                    if success:
                        remaining_unprocessed.remove(selected_filename)
                    
                    if remaining_unprocessed:
                        input("Press Enter : ")
                else:
                    print(f"{Config.COLORS['error_red']} Sélection invalide,{Config.COLORS['reset']}")
                    input(f"{Config.COLORS['error_red']} Press Enter : {Config.COLORS['reset']}")
            else:
                if len(unprocessed_files) == 1:
                    print("Le fichier a été traité")
                else:
                    print("Tous les fichiers ont été traités !")
                input("Press Enter : ")
                break
        
        return self.processed_files, remaining_unprocessed

# ===================================
# SECTION 8: GESTIONNAIRE DE RÉSULTATS
# ===================================

class ResultsDisplayManager:
    """Gestionnaire pour l'affichage des résultats finaux"""
    
    @staticmethod
    def show_initial_results(processed_files, unprocessed_files):
        """Affiche les résultats du traitement automatique initial"""
        if not processed_files:  # Si aucun fichier n'a été traité automatiquement
            print(f"{Config.COLORS['error_red']}Aucun fichier n'a été traité automatiquement. Vérifiez que vos fichiers contiennent date (8 chiffres) et heure (6 chiffres)")
            input(f"Press Enter : {Config.COLORS['reset']}")
            print("\033[A\033[2K\r") 
        
        # Afficher les fichiers traités avec encadré vert
        if processed_files:
            processed_lines = []
            for filename, date in processed_files:
                formatted_line = TextFormatter.format_file_line_with_date(filename, date)
                processed_lines.append(formatted_line)
            title = "FICHIER TRAITÉ" if len(processed_files) == 1 else "FICHIERS TRAITÉS"
            BoxRenderer.print_auto_box(title, "green", processed_lines)
        
        # Message avant affichage des fichiers non traités
        if unprocessed_files:
            if processed_files:  # Ajouter une ligne vide si il y a des fichiers traités
                print()
            
            # Choix du message selon le nombre de fichiers non traités
            if len(unprocessed_files) == 1:
                print("Un fichier n'a pas pu être traité automatiquement")
            elif 2 <= len(unprocessed_files) <= 5:
                print("Quelques fichiers n'ont pas pu être traités automatiquement")
            else:
                print("Certains fichiers n'ont pas pu être traités automatiquement")
            input("Voici la liste des fichiers non traités : ")
            print()
            
            # Déterminer le titre selon le nombre de fichiers (MODE AUTO)
            title = "FICHIER NON TRAITÉ" if len(unprocessed_files) == 1 else "FICHIERS NON TRAITÉS"
            unprocessed_lines = [f" — {filename}" for filename in unprocessed_files]
            BoxRenderer.print_auto_box(title, "red", unprocessed_lines)
            
            print()
            print("Vous allez être rediriger dans l'espace de traitement de fichiers")
            input("Press Enter : ")
    
    @staticmethod
    def show_final_results(auto_processed, manual_processed, unprocessed_files):
        """Affiche le résumé final avec distinction auto/manuel"""
        SystemUtils.clear_screen()
        HeaderRenderer.print_header()
        HeaderRenderer.print_separator()
        
        all_processed = auto_processed + manual_processed
        
        # Afficher tous les fichiers traités avec couleurs distinctes
        if all_processed:
            processed_lines = []
            
            # Fichiers traités automatiquement (vert)
            for filename, date in auto_processed:
                formatted_line = TextFormatter.format_file_line_with_date(filename, date)
                processed_lines.append((formatted_line, "green"))
            
            # Fichiers traités manuellement (jaune)
            for filename, date in manual_processed:
                formatted_line = TextFormatter.format_file_line_with_date(filename, date)
                processed_lines.append((formatted_line, "yellow"))
            
            # Déterminer le titre
            title = "FICHIER TRAITÉ" if len(all_processed) == 1 else "FICHIERS TRAITÉS"
            BoxRenderer.print_mixed_box(title, processed_lines)
        
        # Afficher les fichiers encore non traités - TABLEAU ROUGE SÉPARÉ
        if unprocessed_files:
            if all_processed:
                print()
            
            title = "FICHIER NON TRAITÉ" if len(unprocessed_files) == 1 else "FICHIERS NON TRAITÉS"
            unprocessed_lines = [f" — {filename}" for filename in unprocessed_files]
            BoxRenderer.print_auto_box(title, "red", unprocessed_lines)  # ← TABLEAU ROUGE SÉPARÉ !

# ===================================
# SECTION 9: GESTIONNAIRE PRINCIPAL
# ===================================

class ApplicationManager:
    """Gestionnaire principal de l'application"""
    
    def __init__(self):
        self.auto_processor = AutoProcessor()
        self.manual_processor = ManualProcessor()
    
    def display_directory_info(self, files, current_dir):
        """Affiche les informations sur le répertoire et les fichiers trouvés"""
        message = f"{len(files)} {'fichier' if len(files) == 1 else 'fichiers'} {'trouvé' if len(files) == 1 else 'trouvés'} dans {current_dir}"
        print(message)
        print()
    
    def should_enter_manual_mode(self, unprocessed_files):
        """Détermine si on doit entrer en mode manuel"""
        return len(unprocessed_files) > 0
    
    def show_final_status(self, all_processed_files):
        """Affiche le statut final du traitement"""
        HeaderRenderer.print_separator()
        
        if all_processed_files:
            print("Traitement terminé avec succès !")
            input("Press Enter : ")
        else:
            print(f"{Config.COLORS['error_red']}Aucun fichier n'a pu être traité")
            input(f"Press Enter : {Config.COLORS['reset']}")

# ===================================
# SECTION 10: FONCTIONS LEGACY (COMPATIBILITÉ)
# ===================================

def clear_screen():
    """Efface l'écran de la console"""
    return SystemUtils.clear_screen()

def maximize_cmd():
    """Simule la pression de la touche Alt+Enter pour maximiser la fenêtre CMD"""
    return SystemUtils.maximize_cmd()

def print_header():
    """Affiche l'en-tête du programme avec couleur bleue"""
    return HeaderRenderer.print_header()

def print_progress_bar(current, total, filename=""):
    """Affiche une barre de progression sans scintillement"""
    return ProgressBarRenderer.print_progress_bar(current, total, filename)

def print_manual_header():
    """Affiche l'en-tête pour la modification manuelle"""
    return HeaderRenderer.print_manual_header()

def print_separator():
    """Affiche une ligne de séparation"""
    return HeaderRenderer.print_separator()

def split_long_filename_lines(filename, max_length=125):
    """Découpe un nom de fichier trop long en plusieurs lignes de max_length caractères, avec indentation pour les suivantes."""
    return TextFormatter.split_long_filename_lines(filename, max_length)

def truncate_filename(filename, max_length=80):
    """Tronque le nom de fichier à max_length caractères (strictement supérieur), ajoute '…' si besoin."""
    return TextFormatter.truncate_filename(filename, max_length)

def print_box(title, color_code, content_lines):
    """Affiche un encadré coloré avec titre et contenu (supporte découpage pour fichiers non traités)."""
    return BoxRenderer.print_auto_box(title, color_code, content_lines)

def print_mixed_box(title, content_lines_with_colors):
    """Affiche un encadré avec lignes de couleurs différentes (supporte découpage pour fichiers non traités)."""
    return BoxRenderer.print_mixed_box(title, content_lines_with_colors)

def set_file_timestamp(filename, new_date):
    """Change les dates de création, modification, et accès"""
    return FileSystemUtils.set_file_timestamp(filename, new_date)

def extract_date_from_filename(filename):
    """Extrait la date du nom de fichier"""
    return DateTimeParser.extract_date_from_filename(filename)

def parse_manual_datetime(input_str):
    """Parse une date et heure saisies manuellement avec les formats spécifiques"""
    return DateTimeParser.parse_manual_datetime(input_str)

def manual_timestamp_modification(unprocessed_files):
    """Interface pour modifier manuellement les timestamps"""
    manual_processor = ManualProcessor()
    return manual_processor.manual_timestamp_modification(unprocessed_files)

# ===================================
# SECTION 11: WORKFLOWS & ORCHESTRATION
# ===================================

def auto_timestamp_workflow(files):
    """Gère tout le workflow de traitement automatique"""
    # Initialisation
    app_manager = ApplicationManager()
    current_dir = os.getcwd()
    
    # Affichage des informations
    app_manager.display_directory_info(files, current_dir)
    
    # Traitement automatique avec barre de progression  
    app_manager.auto_processor.process_files_with_progress(files)
    
    # Affichage des résultats initiaux
    HeaderRenderer.print_separator()
    ResultsDisplayManager.show_initial_results(
        app_manager.auto_processor.processed_files,
        app_manager.auto_processor.unprocessed_files
    )
    
    return app_manager

def manual_timestamp_workflow(app_manager):
    """Gère tout le workflow de traitement manuel"""
    manual_processed = []
    
    if app_manager.should_enter_manual_mode(app_manager.auto_processor.unprocessed_files):
        # Modification manuelle
        manual_processed, remaining_unprocessed = app_manager.manual_processor.manual_timestamp_modification(
            app_manager.auto_processor.unprocessed_files
        )
        
        # Mise à jour des listes
        app_manager.auto_processor.unprocessed_files = remaining_unprocessed
        
        # Réaffichage du résumé final
        ResultsDisplayManager.show_final_results(
            app_manager.auto_processor.processed_files,
            manual_processed, 
            remaining_unprocessed
        )
    
    return manual_processed

def process_directory():
    """Point d'entrée principal - Orchestration simple"""
    # 1. Initialisation de l'interface
    SystemUtils.clear_screen()
    SystemUtils.maximize_cmd()
    HeaderRenderer.print_header()
    HeaderRenderer.print_separator()
    
    # 2. Vérification des fichiers
    current_dir = os.getcwd()
    files = FileSystemUtils.get_files_in_directory(current_dir)
    
    if not files:
        print(f'{Config.COLORS["error_red"]}Aucun fichier trouvé dans le répertoire{Config.COLORS["reset"]}')
        input("Press Enter : ")
        return
    
    # 3. Workflow automatique
    app_manager = auto_timestamp_workflow(files)
    
    # 4. Workflow manuel (si nécessaire)  
    manual_processed = manual_timestamp_workflow(app_manager)
    
    # 5. Affichage du statut final
    all_processed = app_manager.auto_processor.processed_files + manual_processed
    app_manager.show_final_status(all_processed)

# ===================================
# SECTION 12: POINT D'ENTRÉE
# ===================================

if __name__ == "__main__":
    process_directory()
