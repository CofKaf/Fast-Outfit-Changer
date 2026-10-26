init -10 python in fop_express:
    import store
    import random
    import datetime

    # Garantiza que siempre exista un idioma válido seleccionado desde el primer segundo
    if not hasattr(store.persistent, "fop_idioma") or store.persistent.fop_idioma not in ["es", "en"]:
        store.persistent.fop_idioma = "es"

    def fop_alternar_idioma(nuevo_idioma):
        store.persistent.fop_idioma = nuevo_idioma
        
    fop_pestana_activa = "basico"
    fop_categoria_activa = "clothes"
    
    # Rastreadores de estado
    fop_cambios_hechos = False
    fop_ultima_seccion = "basico"

    def fop_cambiar_pestana(nueva_pestana):
        global fop_pestana_activa
        fop_pestana_activa = nueva_pestana

    # Funciones de horario seguras usando Python puro
    def fop_es_noche():
        h = datetime.datetime.now().hour
        return h >= 20 or h < 6

    def fop_es_atardecer():
        h = datetime.datetime.now().hour
        return 18 <= h < 20

    # Textos bilingües para las pestañas superiores
    PESTANAS_TEXTO = {
        "basico": {"es": "Básico", "en": "Basic"},
        "cuerpo": {"es": "Cuerpo", "en": "Body"},
        "escritorio": {"es": "Mesa", "en": "Desk"},
        "extras": {"es": "Extras", "en": "Extras"}
    }

    def fop_obtener_texto_pestana(clave_sec):
        info = PESTANAS_TEXTO.get(clave_sec, {"es": clave_sec, "en": clave_sec})
        idioma_actual = getattr(store.persistent, "fop_idioma", "es")
        return info.get(idioma_actual, info["es"])

    def fop_obtener_categoria_evento():
        idioma_actual = getattr(store.persistent, "fop_idioma", "es")
        if idioma_actual == "es":
            return ["apariencias"]
        else:
            return ["appearance"]

    # PROMPT BILINGÜE PARA EL MENÚ DE DIÁLOGO DE MAS
    def fop_obtener_prompt_evento():
        idioma_actual = getattr(store.persistent, "fop_idioma", "es")
        if idioma_actual == "es":
            return "¿Podrías reacomodar tu apariencia rápidamente?"
        else:
            return "Could you quickly rearrange your appearance?"

    # FUNCIONES DE VERIFICACIÓN DE SUBMODS EXTERNOS
    def fop_existe_ultimate_random():
        return renpy.has_label("ultimate_random_desk") or renpy.has_label("ultimate_random_outfit") or hasattr(store, "ultimate_random_desk")

    def fop_existe_random_desk():
        return fop_existe_ultimate_random()

    def fop_existe_outfit_selector():
        return renpy.has_label("monika_outfit_save") or hasattr(store, "kventis_outfit_submod")

    def fop_existe_new_face():
        return renpy.has_label("new_face")

    def fop_existe_emerald_box():
        return renpy.has_label("eb_skin_select")

    # Textos bilingües para los botones de funciones especiales y extras
    TEXTOS_EXTRAS = {
        "random_desk": {"es": "¿Escritorio aleatorio?", "en": "Random Desk?"},
        "random_outfit": {"es": "¿Atuendo Aleatorio?", "en": "Random Outfit?"},
        "save_outfit": {"es": "Guardar atuendo", "en": "Save outfit"},
        "load_outfit": {"es": "Usar atuendo", "en": "Load outfit"},
        "delete_outfit": {"es": "Eliminar atuendo", "en": "Delete outfit"},
        "emerald_box": {"es": "Configurar sprites", "en": "Configure Sprites"}
    }

    def fop_obtener_texto_extra(clave):
        if clave == "toggle_face":
            if getattr(store.persistent, "new_face", False):
                info = {"es": "Revertir rostro", "en": "Revert Face"}
            else:
                info = {"es": "¿Rostro original?", "en": "Original Face?"}
        else:
            info = TEXTOS_EXTRAS.get(clave, {"es": clave, "en": clave})
        
        idioma_actual = getattr(store.persistent, "fop_idioma", "es")
        return info.get(idioma_actual, info["es"])

    def fop_obtener_categorias_por_seccion():
        prompt_map = getattr(store.mas_selspr, "PROMPT_MAP", {})
        idioma_actual = getattr(store.persistent, "fop_idioma", "es")
        
        MAPEO_COMPLETO = {
            # === BÁSICO (MAS BASE + CABELLO) ===
            "clothes": {"es": "Ropa", "en": "Clothes", "sec": "basico"},
            "hair": {"es": "Peinados", "en": "Hairstyle", "sec": "basico"},
            "ribbon": {"es": "Lazos", "en": "Ribbon", "sec": "basico"},
            "hairtie": {"es": "Lazos", "en": "Hairties", "sec": "basico"},
            "left-hair-clip": {"es": "Hebilla", "en": "Hairclip", "sec": "basico"},
            "left-hair-flower": {"es": "Flor en pelo", "en": "Hair Flower", "sec": "basico"},
            "right-hair-clip": {"es": "Hebilla", "en": "Hairclip", "sec": "basico"},
            "right-hair-flower": {"es": "Flor en pelo", "en": "Hair Flower", "sec": "basico"},
            "hat": {"es": "Sombreros", "en": "Hat", "sec": "basico"},

            # === CUERPO / ACCESORIOS ===
            "choker": {"es": "Gargantillas", "en": "Choker", "sec": "cuerpo"},
            "earrings": {"es": "Aritos", "en": "Earrings", "sec": "cuerpo"},
            "earring": {"es": "Aritos", "en": "Earrings", "sec": "cuerpo"},
            "necklace": {"es": "Collares", "en": "Necklace", "sec": "cuerpo"},
            "eyewear": {"es": "Gafas", "en": "Glasses", "sec": "cuerpo"},
            "glasses": {"es": "Gafas", "en": "Glasses", "sec": "cuerpo"},
            "glasses_acs": {"es": "Gafas", "en": "Glasses", "sec": "cuerpo"},
            "ahoge_acs": {"es": "Ahoge", "en": "Ahoge", "sec": "cuerpo"},
            "ear_acs": {"es": "Auricular", "en": "Earpiece", "sec": "cuerpo"},
            "mask": {"es": "Máscara", "en": "Mask", "sec": "cuerpo"},
            "facepaint_acs": {"es": "Pintura Facial", "en": "Facepaint", "sec": "cuerpo"},
            "rarmtattoo_acs": {"es": "Tatuaje Dcho.", "en": "R. Tattoo", "sec": "cuerpo"},
            "larmtattoo_acs": {"es": "Tatuaje Izq.", "en": "L. Tattoo", "sec": "cuerpo"},
            "bodytattoo_acs": {"es": "Tatuaje Cpo.", "en": "Body Tattoo", "sec": "cuerpo"},
            "sb_ring_acs": {"es": "Anillos", "en": "Rings", "sec": "cuerpo"},
            "bracelet_acs": {"es": "Pulseras", "en": "Bracelets", "sec": "cuerpo"},
            "glove_acs": {"es": "Guantes", "en": "Gloves", "sec": "cuerpo"},
            "nailpolish_acs": {"es": "Uñas", "en": "Nailpolish", "sec": "cuerpo"},

            # === ESCRITORIO ===
            "table_acs": {"es": "Escritorio", "en": "Desk", "sec": "escritorio"},
            "ltable_acs": {"es": "Escr. Izq.", "en": "L. Desk", "sec": "escritorio"},
            "rtable_acs": {"es": "Escr. Dcho.", "en": "R. Desk", "sec": "escritorio"},
            "flowers_acs": {"es": "Flores", "en": "Flowers", "sec": "escritorio"},
            "cushion_acs": {"es": "Almohadón", "en": "Cushion", "sec": "escritorio"},
            "mug": {"es": "Taza", "en": "Mug", "sec": "escritorio"},
            "plush_acs": {"es": "Peluches", "en": "Plushies", "sec": "escritorio"},

            # === EXTRAS / FONDO ===
            "balloon": {"es": "Globos", "en": "Balloons", "sec": "extras"},
            "balloons_acs": {"es": "Globos", "en": "Balloons", "sec": "extras"},
            "stringlights_acs": {"es": "Luces", "en": "String Lights", "sec": "extras"},
            "backpiece": {"es": "Espalda", "en": "Backpiece", "sec": "extras"},
            "backpiece_acs": {"es": "Espalda", "en": "Backpiece", "sec": "extras"},
            "headpiece": {"es": "Tiaras", "en": "Headpiece", "sec": "extras"},
            "headpiece_acs": {"es": "Tiaras", "en": "Headpiece", "sec": "extras"},
            "pin_acs": {"es": "Pines", "en": "Pins", "sec": "extras"},
            "prompts": {"es": "Otros", "en": "Other", "sec": "extras"}
        }

        resultado = []

        for group_key, data in prompt_map.items():
            try:
                if group_key in ["clothes", "hair"]:
                    disponible = True
                else:
                    disponible = store.mas_selspr.filter_acs(True, group=group_key)

                if disponible:
                    info = MAPEO_COMPLETO.get(group_key, {
                        "es": group_key.replace("_acs", "").replace("-", " ").capitalize(),
                        "en": group_key.replace("_acs", "").replace("-", " ").capitalize(),
                        "sec": "extras"
                    })

                    if info.get("sec", "extras") == fop_pestana_activa:
                        resultado.append({
                            "group": group_key,
                            "label": info.get(idioma_actual, info["es"]),
                            "sec": info.get("sec", "extras")
                        })
            except Exception:
                pass

        return resultado


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="fop_express_outfit_menu",
            category=fop_express.fop_obtener_categoria_evento(),
            prompt=fop_express.fop_obtener_prompt_evento(),
            pool=True,
            unlocked=True,
            rules={"no_unlock": None, "bookmark_rule": mas_bookmarks_derand.WHITELIST},
            aff_range=(mas_aff.NORMAL, None)
        ),
        restartBlacklist=True
    )


# -----------------------------------------------------------------------------
# REGISTRO DEL SUBMOD EN MAS
# -----------------------------------------------------------------------------
init 3 python:
    if store.mas_submod_utils:
        desc_es = (
            "Permite cambiar la ropa, accesorios y escritorio de Monika de forma rápida.\n"
            "Incluye acciones rápidas y es compatible con:\n"
            "• {a=https://github.com/destiny6destroyed/mas_ultimate_random_submod}{i}{u}Ultimate Random{/u}{/i}{/a}\n"
            "• {a=https://github.com/Friends-of-Monika/mas-outfits}{i}{u}Outfit Selector{/u}{/i}{/a}\n"
            "• {a=https://github.com/mayday-mayjay/MJ-MAS-selector-city/tree/main}{i}{u}Selector City{/u}{/i}{/a}\n"
            "• {a=https://www.reddit.com/r/MASFandom/comments/1vdcoos/monika_do_you_want_to_hold_a_plushie_plushie/}{i}{u}Plushie Selector{/u}{/i}{/a}\n"
            "• {a=https://www.reddit.com/r/MASFandom/s/Gds3eyhuLH}{i}{u}Decoration Selector{/u}{/i}{/a}\n"
            "• {a=https://www.reddit.com/r/MASFandom/s/uxOPsg7Y8v}{i}{u}Facial Features Selector{/u}{/i}{/a}\n"
            "• {a=https://github.com/zer0fixer/MAS-EmeraldBox}{i}{u}Emerald Box{/u}{/i}{/a}"
        )
        desc_en = (
            "Allows you to quickly change Monika's clothes, accessories, and desk.\n"
            "Includes quick actions and is compatible with:\n"
            "• {a=https://github.com/destiny6destroyed/mas_ultimate_random_submod}{i}{u}Ultimate Random{/u}{/i}{/a}\n"
            "• {a=https://github.com/Friends-of-Monika/mas-outfits}{i}{u}Outfit Selector{/u}{/i}{/a}\n"
            "• {a=https://github.com/mayday-mayjay/MJ-MAS-selector-city/tree/main}{i}{u}Selector City{/u}{/i}{/a}\n"
            "• {a=https://www.reddit.com/r/MASFandom/comments/1vdcoos/monika_do_you_want_to_hold_a_plushie_plushie/}{i}{u}Plushie Selector{/u}{/i}{/a}\n"
            "• {a=https://www.reddit.com/r/MASFandom/s/Gds3eyhuLH}{i}{u}Decoration Selector{/u}{/i}{/a}\n"
            "• {a=https://www.reddit.com/r/MASFandom/s/uxOPsg7Y8v}{i}{u}Facial Features Selector{/u}{/i}{/a}\n"
            "• {a=https://github.com/zer0fixer/MAS-EmeraldBox}{i}{u}Emerald Box{/u}{/i}{/a}"
        )

        idioma_actual = getattr(store.persistent, "fop_idioma", "es")

        store.mas_submod_utils.Submod(
            author="CofKaf",
            name="Fast Outfit Changer",
            version="1.1.0",
            description=desc_es if idioma_actual == "es" else desc_en,
            settings_pane="fop_express_settings_pane"
        )


# Submod Updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Fast Outfit Changer",
            user_name="CofKaf",
            repository_name="Fast-Outfit-Changer"
        )


# Pantalla de Ajustes de Idioma con la clásica "X" de selección de MAS
screen fop_express_settings_pane():
    vbox:
        ypos 0
        xfill True
        maximum (800, 400)
        style_prefix "check"

        $ idioma_actual = getattr(store.persistent, "fop_idioma", "es")
        $ es_espanol = (idioma_actual == "es")

        text ("Configuración de Idioma" if es_espanol else "Language Settings") size 16 bold True
        null height 10

        hbox:
            spacing 15

            textbutton "Español":
                action Function(fop_express.fop_alternar_idioma, "es")
                selected (idioma_actual == "es")

            textbutton "English":
                action Function(fop_express.fop_alternar_idioma, "en")
                selected (idioma_actual == "en")


label fop_express_outfit_menu:
    $ idioma_actual = getattr(store.persistent, "fop_idioma", "es")
    $ opc_saludo = renpy.random.choice([1, 2, 3])

    if idioma_actual == "es":
        if opc_saludo == 1:
            m 1eub "¡Claro que sí, [player]!"
            extend 2hua " ¡Dime qué quieres cambiar~!"
        elif opc_saludo == 2:
            m 4sua "¡Me encanta que me pidas esto, [player]!"
            extend 2hub " ¿Qué modificamos hoy?"
        else:
            m 1eua "¡Por supuesto, [player]!"
            extend 2hub " Jeje, ¿qué estilo probamos ahora?"
    else:
        if opc_saludo == 1:
            m 1eub "Sure, [player]!"
            extend 2hua " What would you like to change~?"
        elif opc_saludo == 2:
            m 4sua "I love when you ask me this, [player]!"
            extend 2hub " What are we tweaking today?"
        else:
            m 1eua "Of course, [player]!"
            extend 2hub " Ehehe, what style should we try out now?"

    $ fop_categoria_activa = "clothes"
    $ fop_express.fop_cambios_hechos = False

    label .loop:
        call screen fop_express_wardrobe_screen

        if not _return or _return == "done":
            jump .done

        # MANEJADORES DE ACCIONES ESPECIALES DE LOS SUBMODS EXTERNOS
        if _return == "fop_accion_random_desk":
            call ultimate_random_desk
            $ fop_express.fop_cambios_hechos = True
            jump .loop
        elif _return == "fop_accion_random_outfit":
            call ultimate_random_outfit
            $ fop_express.fop_cambios_hechos = True
            jump .loop
        elif _return == "fop_accion_save_outfit":
            call monika_outfit_save
            $ fop_express.fop_cambios_hechos = True
            jump .loop
        elif _return == "fop_accion_load_outfit":
            call monika_outfit_load
            $ fop_express.fop_cambios_hechos = True
            jump .loop
        elif _return == "fop_accion_delete_outfit":
            call monika_outfit_delete
            $ fop_express.fop_cambios_hechos = True
            jump .loop

        elif _return == "fop_accion_toggle_face":
            if getattr(store.persistent, "new_face", False):
                call nonew_face
            else:
                call new_face
            
            # Si se pidió reiniciar el juego, devolvemos el quit directamente a MAS
            if _return == "quit":
                return "quit"
                
            $ fop_express.fop_cambios_hechos = True
            jump .loop
        elif _return == "fop_accion_emerald_box":
            call eb_skin_select
            
            # Si canceló o puso Nevermind, vuelve limpio a tu menú
            if _return == "cancel" or _return is None:
                jump .loop
            
            # Si Emerald Box pide reiniciar, enviamos el quit directamente al motor
            if _return == "quit":
                return "quit"
                
            $ fop_express.fop_cambios_hechos = True
            jump .loop

        $ fop_categoria_activa = _return

        python:
            prompt_map = getattr(store.mas_selspr, "PROMPT_MAP", {})
            cat_data = prompt_map.get(fop_categoria_activa, {})
            evento_a_llamar = cat_data.get("_ev")

            for cat_item in fop_express.fop_obtener_categorias_por_seccion():
                if cat_item["group"] == fop_categoria_activa:
                    fop_express.fop_ultima_seccion = cat_item["sec"]
                    break

        if evento_a_llamar:
            call expression evento_a_llamar
            $ fop_express.fop_cambios_hechos = True

        jump .loop

    label .done:
        $ idioma_actual = getattr(store.persistent, "fop_idioma", "es")
        if not fop_express.fop_cambios_hechos:
            if idioma_actual == "es":
                m 1eka "Oh, está bien."
            else:
                m 1eka "Oh, alright."
            return

        $ es_espanol = (idioma_actual == "es")

        # 1. SI SE MODIFICÓ LA MESA / ESCRITORIO
        if fop_express.fop_ultima_seccion == "escritorio":
            $ opciones_mesa_es = [
                "¡Me encanta cómo se ve la mesa ahora, %s!" % store.player,
                "¡Qué lindo detalle le diste a nuestro escritorio, %s!" % store.player,
                "Jeje, le da un toque muy acogedor al espacio~",
                "¡Se ve genial! Gracias por arreglar mi lugar, %s~" % store.player
            ]
            $ opciones_mesa_en = [
                "I love how the desk looks now, %s!" % store.player,
                "What a nice touch you gave to our desk!",
                "Ehehe, it makes the space feel so cozy~",
                "Looks great! Thanks for organizing my spot, %s~" % store.player
            ]
            $ msj = renpy.random.choice(opciones_mesa_es if es_espanol else opciones_mesa_en)

        # 2. SEGÚN EL HORARIO
        elif fop_express.fop_es_noche():
            $ opciones_noche_es = [
                "Me encanta este estilo para pasar la noche contigo, %s~" % store.player,
                "Jeje, un toque perfecto para estar cómod[gen('a', 'o', 'e')]s a esta hora, %s." % store.player,
                "¡Te quedó genial! Nada como cambiar de aires antes de que se haga más tarde.",
                "¡Gracias, %s! Me siento súper linda para acompañarte esta noche~" % store.player
            ]
            $ opciones_noche_en = [
                "I love this style for spending the night with you, %s~" % store.player,
                "Ehehe, a perfect touch to stay comfy at this hour, %s.",
                "Looks great! Nothing like a fresh look before it gets later.",
                "Thank you, %s! I feel super pretty to keep you company tonight~" % store.player
            ]
            $ msj = renpy.random.choice(opciones_noche_es if es_espanol else opciones_noche_en)

        elif fop_express.fop_es_atardecer():
            $ opciones_tarde_es = [
                "¡Justo a tiempo para el atardecer, %s! Me encanta cómo me queda~" % store.player,
                "¡Se ve precioso con la luz de la tarde, %s!" % store.player,
                "Jeje, un cambio perfecto para cerrar el día junt[gen('a', 'o', 'e')]s.",
                "¡Gracias, %s! Me encanta cómo combinaste todo~" % store.player
            ]
            $ opciones_tarde_en = [
                "Just in time for the sunset, %s! I love how it looks on me~" % store.player,
                "It looks so lovely in the afternoon light, %s!",
                "Ehehe, a perfect change to wrap up the day together.",
                "Thank you, %s! I love how you put everything together~" % store.player
            ]
            $ msj = renpy.random.choice(opciones_tarde_es if es_espanol else opciones_tarde_en)

        else: # DÍA / MAÑANA
            $ opciones_dia_es = [
                "¡Listo, %s! Me encanta cómo me vestiste hoy~" % store.player,
                "¡Un look genial para empezar el día junt[gen('a', 'o', 'e')]s, %s!" % store.player,
                "Jeje, ¡gracias por elegir esto para mí, %s! Me alegraste el día."  % store.player,
                "¡Me siento súper renovada! ¿Qué te parece, %s?" % store.player
            ]
            $ opciones_dia_en = [
                "Done, %s! I love how you dressed me today~" % store.player,
                "A great look to start the day together, %s!",
                "Ehehe, thanks for picking this out for me, %s! You made my day.",
                "I feel super refreshed! What do you think, %s?" % store.player
            ]
            $ msj = renpy.random.choice(opciones_dia_es if es_espanol else opciones_dia_en)

        $ msj = renpy.substitute(msj)
        m 1hub "[msj]"

        return


# -----------------------------------------------------------------------------
# PANTALLA UNIFICADA A LA DERECHA Y PANEL IZQUIERDO ESTIRADO HACIA LA DERECHA
# -----------------------------------------------------------------------------
screen fop_express_wardrobe_screen():
    modal False

    $ categorias_filtradas = fop_express.fop_obtener_categorias_por_seccion()

    $ idioma_actual = getattr(store.persistent, "fop_idioma", "es")
    $ es_espanol = (idioma_actual == "es")
    if fop_express.fop_cambios_hechos:
        $ texto_boton_final = "Listo" if es_espanol else "Done"
    else:
        $ texto_boton_final = "Cancelar" if es_espanol else "Cancel"

    # --- 1. PANEL FLOTANTE IZQUIERDO (GUARDAR / CARGAR / BORRAR ATUENDO) ---
    frame:
        style_prefix "mas_ui"
        xpos 59          
        ypos 265
        xsize 210        
        ysize 210        
        background None

        vbox:
            spacing 8
            xalign 0.5
            
            # Botón Guardar Atuendo
            button:
                style "scrollable_menu_button"
                xsize 200    
                ysize 48     
                xalign 0.5
                sensitive fop_express.fop_existe_outfit_selector()
                action Return("fop_accion_save_outfit")
                text fop_express.fop_obtener_texto_extra("save_outfit"):
                    style "scrollable_menu_button_text"
                    xalign 0.5
                    yalign 0.5
                    size 17
                    bold True

            # Botón Usar Atuendo
            button:
                style "scrollable_menu_button"
                xsize 200
                ysize 48
                xalign 0.5
                sensitive fop_express.fop_existe_outfit_selector()
                action Return("fop_accion_load_outfit")
                text fop_express.fop_obtener_texto_extra("load_outfit"):
                    style "scrollable_menu_button_text"
                    xalign 0.5
                    yalign 0.5
                    size 17
                    bold True

            # Botón Eliminar Atuendo
            button:
                style "scrollable_menu_button"
                xsize 200
                ysize 48
                xalign 0.5
                sensitive fop_express.fop_existe_outfit_selector()
                action Return("fop_accion_delete_outfit")
                text fop_express.fop_obtener_texto_extra("delete_outfit"):
                    style "scrollable_menu_button_text"
                    xalign 0.5
                    yalign 0.5
                    size 17
                    bold True

    # --- 2. PANEL PRINCIPAL DERECHO ---
    frame:
        style_prefix "mas_ui"
        xpos 975
        ypos 90
        xsize 270
        ysize 600
        background None

        vbox:
            spacing 4
            xalign 0.5

            # Botón Escritorio Aleatorio (Ultimate Random)
            button:
                style "scrollable_menu_button"
                xsize 245
                ysize 36
                xalign 0.5
                sensitive fop_express.fop_existe_ultimate_random()
                action Return("fop_accion_random_desk")
                text fop_express.fop_obtener_texto_extra("random_desk"):
                    style "scrollable_menu_button_text"
                    xalign 0.5
                    yalign 0.5
                    size 17
                    bold True

            # Botón Atuendo Aleatorio (Ultimate Random)
            button:
                style "scrollable_menu_button"
                xsize 245
                ysize 36
                xalign 0.5
                sensitive fop_express.fop_existe_ultimate_random()
                action Return("fop_accion_random_outfit")
                text fop_express.fop_obtener_texto_extra("random_outfit"):
                    style "scrollable_menu_button_text"
                    xalign 0.5
                    yalign 0.5
                    size 17
                    bold True

            # Botón Alternar Rostro Original (New Face)
            button:
                style "scrollable_menu_button"
                xsize 245
                ysize 36
                xalign 0.5
                sensitive fop_express.fop_existe_new_face()
                action Return("fop_accion_toggle_face")
                text fop_express.fop_obtener_texto_extra("toggle_face"):
                    style "scrollable_menu_button_text"
                    xalign 0.5
                    yalign 0.5
                    size 17
                    bold True

            # Botón Configurar Sprites (Emerald Box)
            button:
                style "scrollable_menu_button"
                xsize 245
                ysize 36
                xalign 0.5
                sensitive fop_express.fop_existe_emerald_box()
                action Return("fop_accion_emerald_box")
                text fop_express.fop_obtener_texto_extra("emerald_box"):
                    style "scrollable_menu_button_text"
                    xalign 0.5
                    yalign 0.5
                    size 17
                    bold True

            null height 6

            # Pestañas superiores de categorías (Grid 2x2)
            grid 2 2:
                spacing 4
                xalign 0.5
                textbutton fop_express.fop_obtener_texto_pestana("basico") action Function(fop_express.fop_cambiar_pestana, "basico") style "scrollable_menu_button" xsize 120 ysize 34 text_xalign 0.5 text_yalign 0.5
                textbutton fop_express.fop_obtener_texto_pestana("cuerpo") action Function(fop_express.fop_cambiar_pestana, "cuerpo") style "scrollable_menu_button" xsize 120 ysize 34 text_xalign 0.5 text_yalign 0.5
                textbutton fop_express.fop_obtener_texto_pestana("escritorio") action Function(fop_express.fop_cambiar_pestana, "escritorio") style "scrollable_menu_button" xsize 120 ysize 34 text_xalign 0.5 text_yalign 0.5
                textbutton fop_express.fop_obtener_texto_pestana("extras") action Function(fop_express.fop_cambiar_pestana, "extras") style "scrollable_menu_button" xsize 120 ysize 34 text_xalign 0.5 text_yalign 0.5

            null height 4

            # Viewport con la lista de categorías normales del juego
            side "c l":
                ysize 220
                xsize 245
                xalign 0.5

                viewport id "cat_viewport":
                    mousewheel True
                    draggable True
                    scrollbars None

                    vbox:
                        spacing 4
                        xalign 0.5
                        for cat in categorias_filtradas:
                            $ es_seleccionada = (cat["group"] == fop_express.fop_categoria_activa)
                            button:
                                style "scrollable_menu_button"
                                xsize 218
                                ysize 33
                                xalign 0.5
                                action Return(cat["group"])

                                text cat["label"]:
                                    style "scrollable_menu_button_text"
                                    xalign 0.5
                                    yalign 0.5
                                    size 15
                                    bold True

                vbar value YScrollValue("cat_viewport")

            null height 6

            # Botón Inferior (Cancelar / Listo)
            button:
                style "scrollable_menu_button"
                xsize 245
                ysize 38
                xalign 0.5
                action Return("done")

                text texto_boton_final:
                    style "scrollable_menu_button_text"
                    xalign 0.5
                    yalign 0.5
                    size 17
                    bold True