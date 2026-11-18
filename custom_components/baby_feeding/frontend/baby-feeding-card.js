/* Dashboard card for the Baby Feeding integration: reads sensor.baby_feeding_status, writes through the baby_feeding actions, English with a Dutch translation. */
const BABY_FEEDING_TEXT={"en":{"nav_label":"Feeding navigation","nav_today":"Today","nav_history":"Diary","nav_settings":"Settings","next_bottle":"Next bottle","loading":"Loading…","last_loading":"Loading the last bottle","bottle_form":"Fill in bottle","feed_saved_heading":"Feed saved","recovery_text":"The form is not available yet. Restore it to continue.","restore":"Restore form","saved_check":"✓ Saved","new_feed":"New feed","date":"Date","given_at":"Given at","amount_label":"Amount drunk · ml","aria_minus":"One ml less","aria_plus":"One ml more","save":"Save","add_earlier_feed":"Add earlier feed","overview":"Feeding overview","today_total":"Today total","week_total":"This week total","loading_diary":"Loading diary…","stats_help":"You can change a saved bottle below. The next reminder follows the time you entered.","forecast_title":"Upcoming bottles","forecast_help":"Expected if you keep this rhythm","aria_forecast_list":"Expected bottle times","diary_title":"Feeding diary","aria_history_day":"Day of the feeds","today_button":"Today","refresh":"Refresh","earlier_bottle_button":"+ Earlier bottle","loading_feeds":"Loading feeds…","no_feeds_day":"No feeds saved on this day yet.","edit_feed":"Edit feed","aria_minus_edit":"One ml less for this feed","aria_plus_edit":"One ml more for this feed","cancel":"Cancel","settings_title":"Bottle settings","standard_help":"The default amount is filled in for a new bottle. Saved bottles are not changed.","standard_label":"Default amount · ml","maximum_label":"Agreed maximum · ml, optional","not_set":"Not set","plus_ten":"+ 10 ml","night_rhythm":"Night rhythm","use_custom_night":"Use own night interval","on":"On","off":"Off","night_hours_label":"Time between night feeds · hours","save_settings":"Save settings","invalid_date_time":"Enter a valid date and time.","invalid_date":"Choose a valid date.","dst_gap":"This time does not exist because of the daylight-saving change. Choose the actual time.","rhythm_summary":"Day 3 h · night {hours} h","invalid_amount":"Enter a whole amount between 0 and 9999.","too_far_ahead":"Choose a time no more than 24 hours ahead.","amount_value":"{amount} ml","night_help_on":"From 22:30 to 07:00 the next reminder follows after {hours} hours. By day it stays 3 hours.","night_help_off":"Off: from 22:30 to 07:00 the default {hours} hours applies, 3 hours by day. Your chosen night interval is kept.","today_prefix":"Today · ","tomorrow_prefix":"Tomorrow · ","standard_unavailable":"Default amount not available","assuming_amount":"Assuming {amount} ml per bottle","forecast_no_anchor_context":"The forecast appears after the first saved bottle.","forecast_no_anchor_note":"Enter the actual date, time and amount. No feeds are recorded here.","forecast_no_deadline_context":"The next reminder is not available yet.","forecast_no_deadline_note":"As soon as the plan for the last saved bottle is available, the forecast appears here.","forecast_range":"24 hours from the last saved bottle: {from} to {to}.","marker_next_overdue":"Next · time passed","marker_next":"Next","marker_expected":"Expected","amount_not_set":"amount not set","after_hours":"after {hours} h","forecast_note_overdue":"The first expected time has passed. Save the bottle you actually gave to update this forecast. Later times are only expected; no bottles are ticked off.","forecast_note_expected":"These are expected times, not saved feeds. The times move as soon as you save or change a bottle.","forecast_note_outside":"The next planned bottle falls outside these 24 hours. No feeds were added to the diary.","time_for_bottle":"Time for the bottle","nothing_planned":"No feed planned yet","at_time":"at {time}","bottle_at":"Bottle at {time}","last_bottle":"Last bottle {time}","first_bottle":"Fill in the first bottle","duration_hours":"{n} h","duration_minutes":"{n} min","history_preview":"Earlier feed: the current reminder stays.","earlier_feed_future":"An earlier feed must already have happened. Save a bottle ahead with the bottle form.","more_than_24":"This time is more than 24 hours ahead.","ahead_prefix":"Bottle is set {duration} ahead. ","next_reminder":"Next reminder at {time}{day} · {hours} hours after this bottle.","on_day":" on {date}","rhythm_from_entered":"{rhythm}, counted from the time entered.","not_saved_yet":"Not saved yet","step_above_max":"This step goes above the agreed maximum.","connection_lost":"The connection to Home Assistant was interrupted. Your input is kept; try again.","generic_failure":"This did not work. Your input is kept; try again.","new_not_confirmed":"The new form was not confirmed. Try again.","restored_saved":"Form restored. The last feed is already saved.","restored_open":"Form restored. Enter the actual time and amount.","new_bottle_ready":"New bottle ready. Enter the actual time and amount.","save_not_confirmed":"Saving was not confirmed. Your input is kept; try again.","saved_notice":"Saved · {time} · {amount} ml","load_failed":"Loading feeds failed. Check the connection and tap Refresh.","today_average":"{count} bottles · avg. {avg} ml/bottle","week_average":"Avg. {avg} ml/day entered · {days} days","saved_today":"Saved today","choose_day":"Choose tomorrow or an earlier day.","edit_row_aria":"Edit feed: {day} {time} · {amount} ml","edit_button":"✎ Edit","feed_moved":"This feed was moved or deleted. Tap Refresh.","feed_changed_elsewhere":"This feed was changed on another device. Tap Refresh and open the feed again.","only_planned_ahead":"Choose a time that has passed. Only the last saved bottle can be set ahead.","saved_overview_updating":"The feed was saved. The overview is being updated.","maximum_too_low":"Enter a maximum of at least 1 or leave the field empty.","standard_above_maximum":"The default amount is above the agreed maximum.","night_hours_invalid":"Choose a whole number of night hours from 3 to 8.","settings_not_confirmed":"The settings were not confirmed yet. Your input is kept; try again.","settings_saved":"Settings saved","settings_saved_notice":"Settings saved. The next reminder and the forecast follow the saved rhythm.","open_feeding":"Open feeding","error_bottle_too_far_ahead":"Choose a start time no more than 24 hours ahead.","error_earlier_feed_in_future":"An earlier feed must already have happened. Save a bottle ahead with the bottle form.","error_only_planned_bottle_ahead":"Choose a time that has passed. Only the last saved bottle can be set ahead.","error_invalid_amount":"Enter a whole amount between 0 and 9999.","error_maximum_too_low":"Enter a maximum of at least 1 or leave the field empty.","error_standard_above_maximum":"The default amount is above the agreed maximum.","error_invalid_night_interval":"Choose a whole number of night hours from 3 to 8.","error_minute_taken":"There is already a feed in this minute. Change that feed or choose the actual start time.","error_feed_not_found":"This feed was moved or deleted. Tap Refresh.","error_import_needs_empty_diary":"Importing is only possible into an empty diary.","error_not_loaded":"Baby Feeding is not loaded."},"nl":{"nav_label":"Voeding navigatie","nav_today":"Vandaag","nav_history":"Dagboek","nav_settings":"Instellingen","next_bottle":"Volgende fles","loading":"Laden…","last_loading":"Laatste fles wordt geladen","bottle_form":"Fles invullen","feed_saved_heading":"Voeding opgeslagen","recovery_text":"De invoer is nog niet beschikbaar. Herstel de invoer om verder te gaan.","restore":"Invoer herstellen","saved_check":"✓ Opgeslagen","new_feed":"Nieuwe voeding","date":"Datum","given_at":"Gegeven om","amount_label":"Gedronken hoeveelheid · cc","aria_minus":"Een cc minder","aria_plus":"Een cc meer","save":"Opslaan","add_earlier_feed":"Eerdere voeding toevoegen","overview":"Voedingsoverzicht","today_total":"Vandaag totaal","week_total":"Deze week totaal","loading_diary":"Dagboek laden…","stats_help":"Een opgeslagen fles kun je hieronder aanpassen. De volgende melding volgt de werkelijk ingevulde tijd.","forecast_title":"Komende flessen","forecast_help":"Verwachting als jullie dit ritme aanhouden","aria_forecast_list":"Verwachte flesmomenten","diary_title":"Voedingsdagboek","aria_history_day":"Dag van de voedingen","today_button":"Vandaag","refresh":"Vernieuwen","earlier_bottle_button":"+ Eerdere fles","loading_feeds":"Voedingen laden…","no_feeds_day":"Op deze dag zijn nog geen voedingen opgeslagen.","edit_feed":"Voeding aanpassen","aria_minus_edit":"Een cc minder bij deze voeding","aria_plus_edit":"Een cc meer bij deze voeding","cancel":"Annuleren","settings_title":"Fles instellen","standard_help":"De standaardhoeveelheid wordt ingevuld bij een nieuwe fles. Opgeslagen flessen worden hierdoor niet aangepast.","standard_label":"Standaardhoeveelheid · cc","maximum_label":"Afgesproken maximum · cc, optioneel","not_set":"Niet ingesteld","plus_ten":"+ 10 cc","night_rhythm":"Nachtritme","use_custom_night":"Eigen nachtinterval gebruiken","on":"Aan","off":"Uit","night_hours_label":"Tijd tussen nachtvoedingen · uur","save_settings":"Instellingen opslaan","invalid_date_time":"Vul een geldige datum en tijd in.","invalid_date":"Kies een geldige datum.","dst_gap":"Dit tijdstip bestaat niet door de overgang van zomer- of wintertijd. Kies de werkelijke tijd.","rhythm_summary":"Overdag 3 uur · 's nachts {hours} uur","invalid_amount":"Vul een heel aantal cc in tussen 0 en 9999.","too_far_ahead":"Kies een tijdstip tot uiterlijk 24 uur vooruit.","amount_value":"{amount} cc","night_help_on":"Vanaf 22:30 tot 07:00 volgt de volgende melding na {hours} uur. Overdag blijft het 3 uur.","night_help_off":"Uit: vanaf 22:30 tot 07:00 blijft het standaard {hours} uur, overdag 3 uur. De gekozen nachtduur blijft bewaard.","today_prefix":"Vandaag · ","tomorrow_prefix":"Morgen · ","standard_unavailable":"Standaardhoeveelheid niet beschikbaar","assuming_amount":"Uitgaande van {amount} cc per fles","forecast_no_anchor_context":"De verwachting verschijnt na de eerste opgeslagen fles.","forecast_no_anchor_note":"Vul de werkelijke datum, tijd en hoeveelheid in. Er worden hier geen voedingen geregistreerd.","forecast_no_deadline_context":"De volgende melding is nog niet beschikbaar.","forecast_no_deadline_note":"Zodra de planning bij de laatste opgeslagen fles beschikbaar is, verschijnt de verwachting hier.","forecast_range":"24 uur vanaf de laatste opgeslagen fles: {from} tot {to}.","marker_next_overdue":"Eerstvolgende · tijd verstreken","marker_next":"Eerstvolgende","marker_expected":"Verwacht","amount_not_set":"cc niet ingesteld","after_hours":"na {hours} uur","forecast_note_overdue":"Het eerste verwachte moment is verstreken. Sla de werkelijk gegeven fles op om deze verwachting bij te werken. Latere momenten zijn alleen een verwachting; er zijn geen flessen afgevinkt.","forecast_note_expected":"Dit zijn verwachte momenten, geen opgeslagen voedingen. De tijden schuiven mee zodra jullie een fles opslaan of aanpassen.","forecast_note_outside":"De volgende geplande fles valt buiten deze 24 uur. Er zijn geen voedingen aan het dagboek toegevoegd.","time_for_bottle":"Tijd voor de fles","nothing_planned":"Nog geen voeding gepland","at_time":"om {time}","bottle_at":"Fles om {time}","last_bottle":"Laatste fles {time}","first_bottle":"Vul de eerste fles in","duration_hours":"{n} uur","duration_minutes":"{n} min","history_preview":"Historische voeding: de actuele wekker blijft staan.","earlier_feed_future":"Een eerdere voeding moet al voorbij zijn. Zet een fles vooruit via Fles invullen.","more_than_24":"Dit tijdstip ligt meer dan 24 uur vooruit.","ahead_prefix":"Fles staat {duration} vooruit. ","next_reminder":"Volgende melding om {time}{day} · {hours} uur na deze fles.","on_day":" op {date}","rhythm_from_entered":"{rhythm}, gerekend vanaf de ingevulde tijd.","not_saved_yet":"Nog niet opgeslagen","step_above_max":"Deze stap komt boven het afgesproken maximum.","connection_lost":"De verbinding met Home Assistant is onderbroken. Je invoer blijft staan; probeer opnieuw.","generic_failure":"Dit is niet gelukt. Je invoer blijft staan; probeer opnieuw.","new_not_confirmed":"De nieuwe invoer is niet bevestigd. Probeer opnieuw.","restored_saved":"Invoer hersteld. De laatste voeding is al opgeslagen.","restored_open":"Invoer hersteld. Vul de werkelijke tijd en hoeveelheid in.","new_bottle_ready":"Nieuwe fles klaar. Vul de werkelijke tijd en hoeveelheid in.","save_not_confirmed":"Opslaan is niet bevestigd. Je invoer blijft staan; probeer opnieuw.","saved_notice":"Opgeslagen · {time} · {amount} cc","load_failed":"Voedingen laden lukte niet. Controleer de verbinding en tik op Vernieuwen.","today_average":"{count} flessen · gem. {avg} cc/fles","week_average":"Gem. {avg} cc/ingevoerde dag · {days} dagen","saved_today":"Vandaag opgeslagen","choose_day":"Kies morgen of een eerdere dag.","edit_row_aria":"Voeding wijzigen: {day} {time} · {amount} cc","edit_button":"✎ Wijzig","feed_moved":"Deze voeding is verplaatst of verwijderd. Tik op Vernieuwen.","feed_changed_elsewhere":"Deze voeding is op een ander toestel aangepast. Tik op Vernieuwen en open de voeding opnieuw.","only_planned_ahead":"Kies een tijdstip dat al voorbij is. Alleen de laatst opgeslagen fles kan vooruit staan.","saved_overview_updating":"De voeding is opgeslagen. Het overzicht wordt bijgewerkt.","maximum_too_low":"Vul een maximum van minstens 1 cc in of laat het veld leeg.","standard_above_maximum":"De standaardhoeveelheid ligt boven het afgesproken maximum.","night_hours_invalid":"Kies een heel aantal nachturen van 3 tot en met 8.","settings_not_confirmed":"De instellingen zijn nog niet bevestigd. Je invoer blijft staan; probeer opnieuw.","settings_saved":"Instellingen opgeslagen","settings_saved_notice":"Instellingen opgeslagen. De volgende melding en de verwachting volgen het opgeslagen ritme.","open_feeding":"Voeding openen","error_bottle_too_far_ahead":"Kies een begintijd tot uiterlijk 24 uur vooruit.","error_earlier_feed_in_future":"Een eerdere voeding moet al voorbij zijn. Zet een fles vooruit via Fles invullen.","error_only_planned_bottle_ahead":"Kies een tijdstip dat al voorbij is. Alleen de laatst opgeslagen fles kan vooruit staan.","error_invalid_amount":"Vul een heel aantal cc in tussen 0 en 9999.","error_maximum_too_low":"Vul een maximum van minstens 1 cc in of laat het veld leeg.","error_standard_above_maximum":"De standaardhoeveelheid ligt boven het afgesproken maximum.","error_invalid_night_interval":"Kies een heel aantal nachturen van 3 tot en met 8.","error_minute_taken":"Er staat al een voeding op deze minuut. Pas die voeding aan of kies de werkelijke begintijd.","error_feed_not_found":"Deze voeding is verplaatst of verwijderd. Tik op Vernieuwen.","error_import_needs_empty_diary":"Importeren kan alleen in een leeg dagboek.","error_not_loaded":"Babyvoeding is niet geladen."}};
class BabyFeedingCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({mode:'open'});
    this._mode='main'; this._busy=false; this._draft=null; this._editor=null;
    this._dayRows=[]; this._weekRows=[]; this._dayLoaded=false; this._weekLoaded=false;
    this._selectedDay=''; this._notice=''; this._noticeError=false; this._refreshSequence=0; this._subscriptionGeneration=0;
    this._visible=()=>{if(document.visibilityState==='visible')this._scheduleRefresh();};
    this.shadowRoot.innerHTML=`
      <style>
        :host{display:block;min-width:0;container:feeding / inline-size;--surface:var(--ha-card-background,var(--card-background-color,#1c1c1e));--surface-soft:color-mix(in srgb,var(--primary-text-color,#e8e2dc) 4%,var(--surface));--surface-raised:color-mix(in srgb,var(--primary-text-color,#e8e2dc) 7%,var(--surface));--border:var(--ha-card-border-color,var(--divider-color,#383638));--accent:var(--sh-accent,var(--primary-color,#d88959));--accent-soft:color-mix(in srgb,var(--accent) 16%,var(--surface));--success:var(--sh-ok,var(--success-color,#9bb783));--success-soft:color-mix(in srgb,var(--success) 18%,var(--surface));--danger:var(--sh-alert,var(--error-color,#c96a54));--danger-soft:color-mix(in srgb,var(--danger) 16%,var(--surface));--ink:var(--primary-text-color,#e8e2dc);--muted:var(--secondary-text-color,#a8a19a);font:14px var(--ha-font-family-body,var(--paper-font-body1_-_font-family,system-ui,sans-serif));color:var(--ink)}
        *{box-sizing:border-box}
        ha-card{display:block;min-width:0;border:0;box-shadow:none;background:transparent}
        button,input{font:inherit;-webkit-appearance:none;appearance:none}
        button{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-width:0;min-height:48px;margin:0;border:1px solid var(--border);border-radius:6px;padding:11px 14px;background:var(--surface-raised);color:var(--ink);font-weight:600;line-height:1.3;text-align:center;cursor:pointer;touch-action:manipulation;-webkit-tap-highlight-color:transparent}
        button:disabled{cursor:default;opacity:.5}
        button:focus-visible,input:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
        input{display:block;width:100%;min-width:0;max-width:100%;height:52px;margin:0;border:1px solid var(--border);border-radius:6px;padding:12px;background:var(--surface);color:var(--ink);font-size:17px;line-height:1.25;color-scheme:inherit}
        input[type=date],input[type=time]{text-align:left;font-variant-numeric:tabular-nums}
        input::-webkit-date-and-time-value{min-height:1.25em;text-align:left}
        input::-webkit-datetime-edit{padding:0}
        input[type=number]{-moz-appearance:textfield;appearance:textfield}
        input::-webkit-inner-spin-button,input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}
        input::-webkit-calendar-picker-indicator{flex:none;margin:0 0 0 4px;padding:0;opacity:.65;width:19px;height:19px}
        label{display:block;margin:0 0 8px;font-size:12px;font-weight:650;line-height:1.4;color:var(--muted)}
        [hidden]{display:none!important}
        .app{max-width:1100px;min-width:0;margin:auto;padding:4px}
        .nav{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px;margin:0 0 16px;padding:4px;border:1px solid var(--border);border-radius:6px;background:var(--surface)}
        .nav button{border:0;border-bottom:2px solid transparent;background:transparent;padding:10px 8px;border-radius:3px;white-space:nowrap;color:var(--muted)}
        .nav button[aria-current=page]{border-bottom-color:var(--accent);background:var(--accent-soft);color:var(--ink);box-shadow:none}
        .layout{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:16px}
        .panel{min-width:0;border:1px solid var(--border);border-radius:6px;padding:22px;background:var(--surface);box-shadow:none}
        .panel h2{font-family:var(--ha-font-family-heading,Georgia,serif);font-size:19px;line-height:1.35;margin:0 0 18px;font-weight:500}
        .muted{font-size:12px;line-height:1.55;color:var(--muted);overflow-wrap:anywhere}
        .timer{min-width:0;border:1px solid color-mix(in srgb,var(--accent) 45%,var(--border));border-radius:6px;padding:24px;background:linear-gradient(115deg,var(--accent-soft),var(--surface));color:var(--ink);margin-bottom:16px}
        .timer-top,.timer-bottom{display:flex;justify-content:space-between;gap:12px;align-items:center}
        .timer-top{font-size:14px;line-height:1.4}
        .timer-badge{flex:none;padding:7px 12px;border:1px solid color-mix(in srgb,var(--accent) 45%,var(--border));border-radius:4px;background:var(--accent-soft);color:var(--accent);font-weight:650;font-variant-numeric:tabular-nums;white-space:nowrap}
        .countdown{font-size:clamp(32px,7vw,58px);font-weight:650;letter-spacing:.5px;font-variant-numeric:tabular-nums;line-height:1.15;margin:18px 0;overflow-wrap:normal}
        .timer-bottom{font-size:12px;line-height:1.5;opacity:.85;align-items:flex-start}
        .progress{height:4px;border-radius:0;background:var(--border);margin:16px 0;overflow:hidden}
        .progress span{display:block;height:100%;border-radius:0;background:var(--accent);width:0}
        .app.compact{padding:0}
        .compact .timer{margin-bottom:0}
        .compact .countdown{margin:12px 0}
        .compact .progress{margin:12px 0}
        .timer[role=link]{cursor:pointer;-webkit-tap-highlight-color:transparent}
        .timer[role=link]:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
        .forecast{margin:16px 0 0}
        .forecast-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}
        .forecast-head h2{margin-bottom:6px}
        .forecast-standard{flex:none;border:1px solid var(--border);border-radius:4px;padding:7px 10px;background:var(--surface-raised);color:var(--muted);font-size:12px;line-height:1.4;white-space:nowrap}
        .forecast-context{margin:12px 0 0;font-size:12px;line-height:1.5;color:var(--muted)}
        .forecast-list{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;list-style:none;padding:0;margin:18px 0 0}
        .forecast-item{min-width:0;position:relative;border:1px solid var(--border);border-radius:6px;padding:13px;background:var(--surface-soft)}
        .forecast-item.is-next{border-color:var(--accent);background:var(--accent-soft);box-shadow:none}
        .forecast-item.is-overdue{border-color:var(--danger);background:var(--danger-soft)}
        .forecast-dot{display:block;width:8px;height:8px;margin-bottom:9px;border-radius:50%;background:var(--muted)}
        .is-next .forecast-dot{background:var(--accent)}
        .is-overdue .forecast-dot{background:var(--danger)}
        .forecast-body{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:5px 8px;align-items:center}
        .forecast-day{grid-column:1/-1;min-width:0;font-size:11px;line-height:1.4;color:var(--muted);overflow-wrap:anywhere}
        .forecast-time{font-size:25px;font-weight:650;line-height:1.15;color:var(--ink);font-variant-numeric:tabular-nums;white-space:nowrap}
        .forecast-amount{font-size:13px;font-weight:600;color:var(--muted);white-space:nowrap}
        .forecast-spacing{grid-column:1/-1;font-size:11px;line-height:1.4;color:var(--muted)}
        .forecast-marker{display:inline-block;grid-column:1/-1;margin-bottom:7px;font-size:11px;font-weight:650;color:var(--muted)}
        .is-next .forecast-marker{color:var(--accent)}
        .is-overdue .forecast-marker{color:var(--danger)}
        .forecast-note{margin:14px 0 0;font-size:12px;line-height:1.55;color:var(--muted)}
        .forecast-note.is-overdue{padding:11px 12px;border:1px solid var(--danger);border-radius:6px;background:var(--danger-soft);color:var(--ink)}
        .fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;align-items:end}
        .fields>div{min-width:0}
        .quantity{display:grid;grid-template-columns:54px minmax(0,1fr) 54px;gap:8px;align-items:stretch}
        .quantity input{height:58px;padding:8px 10px;text-align:center;font-size:28px;font-weight:650;font-variant-numeric:tabular-nums}
        .step{width:54px;height:58px;min-height:58px;padding:0;font-size:28px;font-weight:500;line-height:1;background:var(--surface-raised)}
        .amount{margin-top:18px}
        .primary{background:var(--accent);color:var(--text-primary-color,#21120a);border-color:var(--accent);box-shadow:none}
        .save{width:100%;margin-top:18px;min-height:52px;font-size:16px}
        .actions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:18px}
        .actions button{width:100%;min-height:50px}
        .saved{padding:16px;border:1px solid var(--success);border-radius:6px;background:var(--success-soft);color:var(--ink);font-size:16px;line-height:1.5;font-weight:650}
        .saved-meta{font-weight:400;margin-top:5px;font-size:13px;opacity:.9}
        .new{width:100%;margin-top:12px}
        .notice{border:1px solid var(--success);border-radius:6px;background:var(--success-soft);color:var(--ink);padding:13px 16px;margin-bottom:16px;line-height:1.5;overflow-wrap:anywhere}
        .notice.error,.error-message{border-color:var(--danger);background:var(--danger-soft);color:var(--ink)}
        .error-message{margin-top:12px;border-radius:12px;padding:12px;font-size:13px;line-height:1.5;overflow-wrap:anywhere}
        .stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
        .stats>div{min-width:0}
        .stats>div+div{border-left:1px solid var(--border);padding-left:18px}
        .stat-label{font-size:13px;line-height:1.5;color:var(--muted)}
        .stat-value{font-size:30px;line-height:1.2;font-weight:650;font-variant-numeric:tabular-nums;margin:9px 0;overflow-wrap:anywhere}
        .stat-value small{font-size:16px}
        .history{margin-top:16px}
        .toolbar{display:grid;grid-template-columns:minmax(155px,190px) auto auto auto;justify-content:start;align-items:stretch;gap:8px;margin-bottom:16px}
        .toolbar input{width:100%;height:48px;font-size:16px}
        .toolbar button{white-space:nowrap}
        .row{display:grid;grid-template-columns:60px minmax(0,1fr) 64px;gap:12px;width:100%;align-items:center;padding:12px 4px;border:0;border-bottom:1px solid var(--border);background:transparent;border-radius:0;text-align:left;min-height:60px;color:inherit}
        .row:last-child{border-bottom:0}
        .row:hover,.row[aria-expanded=true]{background:var(--surface-soft);border-radius:4px}
        .row-time{font-size:16px;font-weight:650;font-variant-numeric:tabular-nums}
        .row-cc{justify-self:end;border:1px solid var(--border);background:var(--surface-raised);color:var(--ink);padding:7px 11px;border-radius:4px;font-weight:650;font-variant-numeric:tabular-nums;white-space:nowrap}
        .row-change{justify-self:end;color:var(--muted);font-size:12px;white-space:nowrap}
        .editor{min-width:0;padding:18px;border:1px solid var(--border);border-radius:6px;background:var(--surface-soft);color:var(--ink);margin:14px 0 0;scroll-margin-top:72px}
        .editor h3{font-size:16px;line-height:1.4;margin:0 0 18px}
        .editor .primary{background:var(--success);border-color:var(--success)}
        .settings{max-width:650px;margin:auto}
        .settings .fields{margin-bottom:16px}
        .settings-status{margin-top:12px;font-size:13px;color:var(--muted)}
        .night-settings{margin-top:24px;padding-top:20px;border-top:1px solid var(--border)}
        .night-heading{display:flex;align-items:center;justify-content:space-between;gap:14px}
        .night-settings h3{margin:0 0 14px;font-size:16px;line-height:1.4;font-weight:600}
        .night-control-label{font-weight:600;line-height:1.5}
        .night-switch{flex:none;gap:9px;min-width:104px}
        .night-switch-track{display:block;width:36px;height:22px;border-radius:12px;padding:3px;background:var(--border)}
        .night-switch-knob{display:block;width:16px;height:16px;border-radius:50%;background:var(--ink);transition:transform .15s ease}
        .night-switch[aria-checked=true]{border-color:var(--accent);background:var(--accent-soft)}
        .night-switch[aria-checked=true] .night-switch-track{background:var(--accent)}
        .night-switch[aria-checked=true] .night-switch-knob{background:var(--surface);transform:translateX(14px)}
        .night-duration{max-width:250px;margin-top:16px}
        .night-duration:has(input:disabled){opacity:.6}
        .loading{padding:12px 0;color:var(--muted);font-size:13px}
        .pill{display:inline-block;padding:7px 11px;border:1px solid var(--border);border-radius:4px;background:var(--surface-raised);font-size:12px;line-height:1.5;color:var(--muted);margin-bottom:12px}
        @container feeding (min-width:601px) and (max-width:850px){
          .forecast-list{grid-template-columns:repeat(2,minmax(0,1fr))}
        }
        @container feeding (max-width:600px){
          .app{padding:0 0 8px}
          .panel{padding:18px;border-radius:6px}
          .nav{margin-bottom:14px}
          .nav button{font-size:13px}
          .timer{padding:20px;margin-bottom:14px}
          .forecast{margin:14px 0 0}
          .forecast-head{display:block}
          .forecast-standard{display:inline-block;margin-top:10px}
          .forecast-list{display:block;margin-top:14px}
          .forecast-item{display:grid;grid-template-columns:10px minmax(0,1fr);gap:13px;border:0;border-radius:0;padding:12px 11px;background:transparent}
          .forecast-item::after{content:"";position:absolute;left:15px;top:25px;bottom:-13px;width:1px;background:var(--border)}
          .forecast-item:last-child::after{display:none}
          .forecast-item.is-next{border:1px solid var(--accent);border-radius:6px;padding:13px 11px;margin:0 0 3px;background:var(--accent-soft)}
          .forecast-item.is-next::after{left:15px}
          .forecast-item.is-overdue{border-color:var(--danger);background:var(--danger-soft)}
          .forecast-dot{width:8px;height:8px;margin:5px 0 0;z-index:1}
          .forecast-body{gap:4px 10px}
          .forecast-day{grid-column:1;grid-row:1;font-size:12px}
          .forecast-time{grid-column:1;grid-row:2;font-size:24px}
          .forecast-amount{grid-column:2;grid-row:2;font-size:14px}
          .forecast-spacing{grid-column:1/-1;grid-row:3}
          .forecast-marker{grid-column:1/-1;margin:0 0 2px;grid-row:1}
          .forecast-item:not(.is-next) .forecast-marker{display:none}
          .is-next .forecast-day{grid-row:2}
          .is-next .forecast-time,.is-next .forecast-amount{grid-row:3}
          .is-next .forecast-spacing{grid-row:4}
          .timer-bottom{display:grid;gap:4px}
          .layout{grid-template-columns:minmax(0,1fr);gap:14px}
          .countdown{font-size:38px}
          .toolbar{grid-template-columns:repeat(2,minmax(0,1fr));justify-content:stretch}
          .toolbar input{grid-column:1/-1}
          .toolbar button:last-child{grid-column:1/-1}
          .history{margin-top:14px}
          .editor{padding:16px}
          .fields{gap:10px}
          input[type=date],input[type=time]{font-size:16px;padding:10px 8px}
          .settings .fields{grid-template-columns:minmax(0,1fr);gap:16px}
          .stats{gap:12px}
          .stats>div+div{padding-left:12px}
          .stat-value{font-size:27px}
        }
        @container feeding (max-width:340px){
          .panel{padding:15px}
          .nav button{font-size:12px;padding-inline:4px}
          .timer{padding:18px}
          .countdown{font-size:32px}
          .fields{grid-template-columns:minmax(0,1fr)}
          .quantity{grid-template-columns:48px minmax(0,1fr) 48px;gap:6px}
          .step{width:48px}
          .row{grid-template-columns:54px minmax(0,1fr) 58px;gap:8px}
          .row-change{font-size:11px}
        }
      </style>
      <ha-card><div class="app">
        <nav class="nav" aria-label="Feeding navigation" data-i18n-aria="nav_label"><button data-action="mode-main"><span data-i18n="nav_today">Today</span></button><button data-action="mode-history"><span data-i18n="nav_history">Diary</span></button><button data-action="mode-settings"><span data-i18n="nav_settings">Settings</span></button></nav>
        <div id="notice" class="notice" role="status" hidden></div>
        <section id="main">
          <div class="timer"><div class="timer-top"><span><span data-i18n="next_bottle">Next bottle</span></span><span id="deadline" class="timer-badge"></span></div><div id="countdown" class="countdown"><span data-i18n="loading">Loading…</span></div><div class="progress"><span id="progress"></span></div><div class="timer-bottom"><span id="last-feed"><span data-i18n="last_loading">Loading the last bottle</span></span><span id="timer-rhythm"></span></div></div>
          <div class="layout"><section class="panel"><h2 id="entry-heading"><span data-i18n="bottle_form">Fill in bottle</span></h2>
            <div id="recovery" hidden><p class="muted"><span data-i18n="recovery_text">The form is not available yet. Restore it to continue.</span></p><button data-action="recover"><span data-i18n="restore">Restore form</span></button></div>
            <div id="saved" hidden><div class="saved"><span data-i18n="saved_check">✓ Saved</span><div id="saved-meta" class="saved-meta"></div></div><button class="new" data-action="new"><span data-i18n="new_feed">New feed</span></button></div>
            <form id="current-form" novalidate><div class="fields"><div><label for="current-date"><span data-i18n="date">Date</span></label><input id="current-date" type="date" required></div><div><label for="current-time"><span data-i18n="given_at">Given at</span></label><input id="current-time" type="time" step="60" required></div></div><div class="amount"><label for="current-amount"><span data-i18n="amount_label">Amount drunk · ml</span></label><div class="quantity"><button type="button" class="step" data-action="current-minus" aria-label="One ml less" data-i18n-aria="aria_minus">−</button><input id="current-amount" type="number" min="0" max="9999" step="1" inputmode="numeric" required><button type="button" class="step" data-action="current-plus" aria-label="One ml more" data-i18n-aria="aria_plus">+</button></div></div><div id="current-preview" class="muted" style="margin-top:11px"></div><div id="current-error" class="error-message" role="alert" hidden></div><button class="primary save" type="submit" data-write><span data-i18n="save">Save</span></button></form>
            <button data-action="add-history" style="width:100%;margin-top:12px"><span data-i18n="add_earlier_feed">Add earlier feed</span></button>
          </section><section class="panel"><h2><span data-i18n="overview">Feeding overview</span></h2><div class="stats"><div><div class="stat-label"><span data-i18n="today_total">Today total</span></div><div id="today-total" class="stat-value">—</div><div id="today-average" class="muted"><span data-i18n="loading_diary">Loading diary…</span></div></div><div><div class="stat-label"><span data-i18n="week_total">This week total</span></div><div id="week-total" class="stat-value">—</div><div id="week-average" class="muted"><span data-i18n="loading_diary">Loading diary…</span></div></div></div><p class="muted" style="margin:18px 0 0"><span data-i18n="stats_help">You can change a saved bottle below. The next reminder follows the time you entered.</span></p></section></div>
          <section id="forecast" class="panel forecast" aria-labelledby="forecast-title"><div class="forecast-head"><div><h2 id="forecast-title"><span data-i18n="forecast_title">Upcoming bottles</span></h2><div class="muted"><span data-i18n="forecast_help">Expected if you keep this rhythm</span></div></div><span id="forecast-standard" class="forecast-standard"></span></div><p id="forecast-context" class="forecast-context"></p><ol id="forecast-list" class="forecast-list" aria-label="Expected bottle times" data-i18n-aria="aria_forecast_list"></ol><p id="forecast-note" class="forecast-note"></p></section>
        </section>
        <section id="history" class="panel history"><h2 id="history-title"><span data-i18n="diary_title">Feeding diary</span></h2><div class="toolbar"><input id="history-day" type="date" aria-label="Day of the feeds" data-i18n-aria="aria_history_day"><button data-action="today"><span data-i18n="nav_today">Today</span></button><button data-action="refresh"><span data-i18n="refresh">Refresh</span></button><button data-action="add-history"><span data-i18n="earlier_bottle_button">+ Earlier bottle</span></button></div><div id="history-loading" class="loading" hidden><span data-i18n="loading_feeds">Loading feeds…</span></div><div id="history-error" class="error-message" role="alert" hidden></div><div id="history-empty" class="loading" hidden><span data-i18n="no_feeds_day">No feeds saved on this day yet.</span></div><div id="history-list"></div>
          <form id="history-editor" class="editor" novalidate hidden><h3 id="editor-heading"><span data-i18n="edit_feed">Edit feed</span></h3><div class="fields"><div><label for="edit-date"><span data-i18n="date">Date</span></label><input id="edit-date" type="date" required></div><div><label for="edit-time"><span data-i18n="given_at">Given at</span></label><input id="edit-time" type="time" step="60" required></div></div><div class="amount"><label for="edit-amount"><span data-i18n="amount_label">Amount drunk · ml</span></label><div class="quantity"><button type="button" class="step" data-action="edit-minus" aria-label="One ml less for this feed" data-i18n-aria="aria_minus_edit">−</button><input id="edit-amount" type="number" min="0" max="9999" step="1" inputmode="numeric" required><button type="button" class="step" data-action="edit-plus" aria-label="One ml more for this feed" data-i18n-aria="aria_plus_edit">+</button></div></div><div id="edit-preview" class="muted" style="margin-top:11px"></div><div id="edit-error" class="error-message" role="alert" hidden></div><div class="actions"><button type="button" data-action="cancel-edit"><span data-i18n="cancel">Cancel</span></button><button class="primary" type="submit" data-write><span data-i18n="save">Save</span></button></div></form>
        </section>
        <section id="settings" class="panel settings" hidden><h2><span data-i18n="settings_title">Bottle settings</span></h2><div id="settings-rhythm" class="pill"></div><p class="muted"><span data-i18n="standard_help">The default amount is filled in for a new bottle. Saved bottles are not changed.</span></p><form id="settings-form" novalidate><div class="fields"><div><label for="standard-amount"><span data-i18n="standard_label">Default amount · ml</span></label><input id="standard-amount" type="number" min="0" max="9999" step="1" inputmode="numeric"></div><div><label for="maximum-amount"><span data-i18n="maximum_label">Agreed maximum · ml, optional</span></label><input id="maximum-amount" type="number" min="1" max="9999" step="1" inputmode="numeric" placeholder="Not set" data-i18n-placeholder="not_set"></div></div><button type="button" data-action="standard-plus"><span data-i18n="plus_ten">+ 10 ml</span></button><section class="night-settings" aria-labelledby="night-title"><h3 id="night-title"><span data-i18n="night_rhythm">Night rhythm</span></h3><div class="night-heading"><span class="night-control-label"><span data-i18n="use_custom_night">Use own night interval</span></span><button id="night-toggle" type="button" class="night-switch" role="switch" aria-checked="true" aria-label="Use own night interval" data-i18n-aria="use_custom_night" aria-describedby="night-help" data-action="night-toggle"><span class="night-switch-track" aria-hidden="true"><span class="night-switch-knob"></span></span><span id="night-toggle-label"><span data-i18n="on">On</span></span></button></div><div class="night-duration"><label for="night-hours"><span data-i18n="night_hours_label">Time between night feeds · hours</span></label><input id="night-hours" type="number" min="3" max="8" step="1" inputmode="numeric" aria-describedby="night-help"></div><p id="night-help" class="muted"></p></section><button class="primary save" type="submit" data-write><span data-i18n="save_settings">Save settings</span></button><div id="settings-error" class="error-message" role="alert" hidden></div><div id="settings-status" class="settings-status"></div></form></section>
      </div></ha-card>`;
    this.$=id=>this.shadowRoot.getElementById(id);
    this.shadowRoot.addEventListener('click',event=>this._onClick(event));
    this.shadowRoot.addEventListener('input',event=>this._onInput(event));
    this.shadowRoot.addEventListener('change',event=>{if(event.target.id==='history-day')this._changeDay(event.target.value);});
    this.shadowRoot.addEventListener('keydown',event=>{if(['INPUT','SELECT','TEXTAREA'].includes(event.target.tagName))event.stopPropagation();else if(['Enter',' '].includes(event.key)&&event.target.closest('.timer')&&this._path()){event.preventDefault();this._open();}});
    this.$('current-form').addEventListener('submit',event=>{event.preventDefault();this._saveCurrent();});
    this.$('history-editor').addEventListener('submit',event=>{event.preventDefault();this._saveHistory();});
    this.$('settings-form').addEventListener('submit',event=>{event.preventDefault();this._saveSettings();});
  }
  setConfig(config){this._config=config||{};this._mode=['main','history','settings','timer'].includes(config?.mode)?config.mode:'main';this._renderMode();}
  getCardSize(){return this._mode==='timer'?3:this._mode==='settings'?7:15;}
  getLayoutOptions(){return {grid_columns:12,grid_rows:'auto'};}
  set hass(hass){
    const previous=this._hass;this._hass=hass;
    if(!hass)return;
    this._applyLanguage();this._syncFields();this._patch();this._subscribe();
    const sensor=hass.states['sensor.baby_feeding_status'];
    const signature=JSON.stringify(sensor?.attributes?.feeds||[]);
    if(this._sensorSignature!==signature){this._sensorSignature=signature;if(previous)this._scheduleRefresh();}
    if(!this._initialRequested&&this.isConnected){this._initialRequested=true;this._refreshAll();}
  }
  connectedCallback(){this._timer=setInterval(()=>this._tick(),1000);document.addEventListener('visibilitychange',this._visible);this._subscribe();if(this._hass){this._initialRequested=true;this._refreshAll();}}
  disconnectedCallback(){this._subscriptionGeneration++;clearInterval(this._timer);clearTimeout(this._refreshTimeout);document.removeEventListener('visibilitychange',this._visible);if(this._unsubscribe)this._unsubscribe();this._unsubscribe=null;this._subscriptionPending=false;}
  _zone(){return this._hass?.config?.time_zone||'Europe/Amsterdam';}
  _lang(){const language=String(this._hass?.locale?.language||this._hass?.language||'en').toLowerCase();return language.startsWith('nl')?'nl':'en';}
  _locale(){return this._lang()==='nl'?'nl-NL':String(this._hass?.locale?.language||'en-GB');}
  _t(key,values={}){const text=BABY_FEEDING_TEXT[this._lang()][key]??BABY_FEEDING_TEXT.en[key]??key;return text.replace(/\{(\w+)\}/g,(_,name)=>String(values[name]??''));}
  _applyLanguage(){const language=this._lang();if(this._appliedLanguage===language)return;this._appliedLanguage=language;for(const element of this.shadowRoot.querySelectorAll('[data-i18n]'))element.textContent=this._t(element.dataset.i18n);for(const element of this.shadowRoot.querySelectorAll('[data-i18n-aria]'))element.setAttribute('aria-label',this._t(element.dataset.i18nAria));for(const element of this.shadowRoot.querySelectorAll('[data-i18n-placeholder]'))element.setAttribute('placeholder',this._t(element.dataset.i18nPlaceholder));this._forecastSignature=null;if(this._dayLoaded)this._renderRows();}
  _status(){return this._hass?.states['sensor.baby_feeding_status'];}
  // Internal keys map the integration's status attributes onto the values the card's planning code works with.
  _state(id){const status=this._status(),a=status?.attributes||{},plan=a.plan,epoch=value=>value?String(Math.floor(Date.parse(value)/1000)):'';switch(id){
    case 'plan_anchor':return plan?`${plan.feed_id}|${epoch(plan.feed_start)}|${epoch(plan.due)}`:'none';
    case 'reminder':return plan?(plan.alerted&&Date.parse(plan.due)<=Date.now()?'alerted:':'')+epoch(plan.due):'unknown';
    case 'session':return status?.state==='open'?(epoch(a.open_start)||'1'):'1';
    case 'saved_marker':return status?.state==='saved'?'1':'none';
    case 'open_start':return epoch(a.open_start)||'none';
    case 'standard_amount':case 'draft_amount':return a.standard_amount===undefined?undefined:String(a.standard_amount);
    case 'maximum_amount':return a.maximum_amount==null?'':String(a.maximum_amount);
    case 'night_custom':return status?(a.night_custom_enabled?'on':'off'):undefined;
    case 'night_hours':return a.night_hours===undefined?undefined:String(a.night_hours);
    default:return this._hass?.states[id]?.state;}}
  _number(id,fallback=0){const value=Number(this._state(id));return Number.isFinite(value)?value:fallback;}
  _parts(stamp){const p=Object.fromEntries(new Intl.DateTimeFormat('sv-SE',{timeZone:this._zone(),year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'}).formatToParts(new Date(stamp)).map(part=>[part.type,part.value]));return {day:`${p.year}-${p.month}-${p.day}`,time:`${p.hour}:${p.minute}`,second:p.second};}
  _localEpoch(day,time,preferred){
    if(!/^\d{4}-\d{2}-\d{2}$/.test(day)||!/^([01]\d|2[0-3]):[0-5]\d$/.test(time))throw Error(this._t('invalid_date_time'));
    const [year,month,date]=day.split('-').map(Number),[hour,minute]=time.split(':').map(Number);
    const wall=Date.UTC(year,month-1,date,hour,minute,0);
    if(new Date(wall).toISOString().slice(0,10)!==day)throw Error(this._t('invalid_date'));
    const matches=stamp=>{const p=this._parts(stamp);return p.day===day&&p.time===time&&p.second==='00';};
    if(Number.isFinite(preferred)&&matches(preferred))return preferred/1000;
    let guess=wall;
    for(let i=0;i<4;i++){const p=this._parts(guess),[y,m,d]=p.day.split('-').map(Number),[h,n]=p.time.split(':').map(Number);const delta=wall-Date.UTC(y,m-1,d,h,n,Number(p.second));guess+=delta;if(!delta)break;}
    const options=[];for(let delta=-7200000;delta<=7200000;delta+=1800000){const value=guess+delta;if(matches(value))options.push(value);}
    const past=options.filter(value=>value<=Date.now());const selected=past.length?Math.max(...past):options[0];
    if(!Number.isFinite(selected))throw Error(this._t('dst_gap'));
    return selected/1000;
  }
  _nightPolicy(){
    const defaultHours=4,rawHours=Number(this._state('night_hours'));
    const selectedHours=Number.isInteger(rawHours)&&rawHours>=3&&rawHours<=8?rawHours:defaultHours;
    const active=this._state('night_custom')==='on';
    return {active,hours:active?selectedHours:defaultHours,selectedHours,defaultHours};
  }
  _rhythmSummary(){return this._t('rhythm_summary',{hours:this._nightPolicy().hours});}
  _interval(epoch){const time=this._parts(epoch*1000).time;return time>='22:30'||time<'07:00'?this._nightPolicy().hours:3;}
  _validAmount(value){if(!String(value).trim()||!Number.isSafeInteger(Number(value))||Number(value)<0||Number(value)>9999)throw Error(this._t('invalid_amount'));return Number(value);}
  _validMoment(day,time,preferred){const epoch=this._localEpoch(day,time,preferred);if(epoch>Date.now()/1000+86400)throw Error(this._t('too_far_ahead'));return epoch;}
  _syncFields(){
    const session=this._state('session')||'';
    const standard=this._number('standard_amount',20);
    const actual=this._number('draft_amount',standard);
    if(!this._draft||this._draft.session!==session){const pending=this._number('open_start',0);const parts=this._parts(pending>0?pending*1000:Date.now());this._draft={session,...parts,amount:String(actual),baselineAmount:String(actual),dirtyAmount:false,dirtyTime:false};this._setCurrentFields();}
    else if(this._lastStandard!==undefined&&standard!==this._lastStandard&&!this._draft.dirtyAmount&&Number(this._draft.amount)===this._lastStandard){this._draft.amount=String(standard);this._draft.baselineAmount=String(standard);this.$('current-amount').value=this._draft.amount;}
    this._lastStandard=standard;
    if(!this._settingsDirty){this.$('standard-amount').value=String(standard);this.$('maximum-amount').value=this._state('maximum_amount')||'';}
    if(!this._nightDirty){const night=this._nightPolicy();this._nightDraft={active:night.active,hours:String(night.selectedHours)};this.$('night-hours').value=this._nightDraft.hours;}
    const today=this._parts(Date.now()).day;
    if(!this._selectedDay){this._selectedDay=today;this.$('history-day').value=today;}
    for(const id of ['current-date','edit-date','history-day'])this.$(id).max=this._tomorrow();
  }
  _tomorrow(){return new Date(Date.parse(this._parts(Date.now()).day+'T12:00:00Z')+86400000).toISOString().slice(0,10);}
  _setCurrentFields(){if(!this._draft)return;this.$('current-date').value=this._draft.day;this.$('current-time').value=this._draft.time;this.$('current-amount').value=this._draft.amount;}
  _patch(){
    this._renderMode();this._tick();this._patchCurrent();this._patchStats();
    const valid=Number(this._draft?.session)>0,stored=this._number('saved_marker',0)>0;
    this.$('recovery').hidden=valid;this.$('saved').hidden=!valid||!stored;this.$('current-form').hidden=!valid||stored;
    this.$('entry-heading').textContent=this._t(stored?'feed_saved_heading':'bottle_form');
    const anchor=(this._state('plan_anchor')||'').split('|');const row=this._weekRows.find(item=>item.description===anchor[0]&&Date.parse(item.start)/1000===Number(anchor[1]))||(this._hass?.states['sensor.baby_feeding_status']?.attributes?.feeds||[]).map(item=>({...item,cc:item.amount})).find(item=>item.id===anchor[0]&&Date.parse(item.start)/1000===Number(anchor[1]));
    const stamp=Number(anchor[1]);this.$('saved-meta').textContent=(stamp>0?this._parts(stamp*1000).time+' · ':'')+this._t('amount_value',{amount:row?.cc??this._draft?.confirmedAmount??this._number('draft_amount',20)});
    for(const el of this.shadowRoot.querySelectorAll('button[data-write],button[data-action],#current-form input,#history-editor input,#settings-form input'))el.disabled=this._busy;
    this._updateSteps();this._patchNightSettings();
    this.$('notice').hidden=this._mode==='timer'||!this._notice;this.$('notice').textContent=this._notice;this.$('notice').classList.toggle('error',this._noticeError);
  }
  _patchNightSettings(){
    const policy=this._nightPolicy(),draft=this._nightDraft||{active:policy.active,hours:String(policy.selectedHours)};
    this.$('night-toggle').setAttribute('aria-checked',String(draft.active));
    this.$('night-toggle-label').textContent=this._t(draft.active?'on':'off');
    const hours=Number(draft.hours),validHours=String(draft.hours).trim()!==''&&Number.isInteger(hours)&&hours>=3&&hours<=8;
    this.$('night-hours').disabled=this._busy||!draft.active&&validHours;
    this.$('night-help').textContent=draft.active?this._t('night_help_on',{hours:draft.hours||'…'}):this._t('night_help_off',{hours:policy.defaultHours});
    this.$('timer-rhythm').textContent=this._rhythmSummary();
    this.$('settings-rhythm').textContent=this._rhythmSummary();
  }
  _renderMode(){if(!this.$)return;const timer=this._mode==='timer';this.$('main').hidden=!timer&&this._mode!=='main';this.$('history').hidden=timer||this._mode==='settings';this.$('settings').hidden=this._mode!=='settings';for(const selector of ['.nav','.layout','#forecast'])this.shadowRoot.querySelector(selector).hidden=timer;this.shadowRoot.querySelector('.app').classList.toggle('compact',timer);const clock=this.shadowRoot.querySelector('.timer');for(const [name,value]of[['role','link'],['tabindex','0'],['aria-label',this._t('open_feeding')]]){if(this._path())clock.setAttribute(name,value);else clock.removeAttribute(name);}for(const button of this.shadowRoot.querySelectorAll('.nav button'))button.setAttribute('aria-current',button.dataset.action==='mode-'+this._mode?'page':'false');}
  _forecastSource(){
    const anchorParts=(this._state('plan_anchor')||'').split('|');
    const anchor=Number(anchorParts[1]),raw=this._state('reminder')||'';
    const claimed=raw.startsWith('alerted:')?Number(raw.slice(7)):0;
    const current=Number(raw),stored=Number(anchorParts[2]);
    const valid=value=>Number.isFinite(value)&&value>0&&Math.abs(value*1000)<=8640000000000000;
    const deadline=valid(claimed)?claimed:valid(current)?current:valid(stored)?stored:raw==='alerted'&&valid(anchor)?anchor+this._interval(anchor)*3600:0;
    return {anchor,deadline};
  }
  _forecastPlan(){
    const {anchor,deadline}=this._forecastSource();
    const validEpoch=value=>Number.isFinite(value)&&value>0&&Math.abs(value*1000)<=8640000000000000-86400000;
    if(!validEpoch(anchor))return {status:'no-anchor',items:[]};
    if(!validEpoch(deadline)||deadline<=anchor)return {status:'no-deadline',anchor,items:[]};
    const standardRaw=this._state('standard_amount');
    const standard=standardRaw!==undefined&&String(standardRaw).trim()!==''&&Number.isFinite(Number(standardRaw))?Number(standardRaw):null;
    const end=anchor+24*3600,items=[];
    let expected=deadline,previous=anchor;
    while(expected<=end&&items.length<12){
      items.push({epoch:expected,intervalHours:(expected-previous)/3600,cc:standard});
      previous=expected;
      expected+=this._interval(expected)*3600;
    }
    return {status:'ready',anchor,deadline,end,standard,items,overdue:deadline<=Date.now()/1000};
  }
  _forecastDayLabel(epoch){
    const day=this._parts(epoch*1000).day,today=this._parts(Date.now()).day;
    const tomorrow=new Date(Date.parse(today+'T12:00:00Z')+86400000).toISOString().slice(0,10);
    const date=new Date(epoch*1000).toLocaleDateString(this._locale(),{timeZone:this._zone(),weekday:'short',day:'numeric',month:'short'});
    return (day===today?this._t('today_prefix'):day===tomorrow?this._t('tomorrow_prefix'):'')+date;
  }
  _patchForecast(){
    const nowDay=this._parts(Date.now()).day;
    const raw=this._state('reminder')||'';
    const boundary=this._forecastSource().deadline;
    const signature=JSON.stringify([this._zone(),this._state('plan_anchor'),raw,this._state('standard_amount'),this._state('night_custom'),this._state('night_hours'),nowDay,boundary>0&&boundary<=Date.now()/1000]);
    if(signature===this._forecastSignature)return;
    this._forecastSignature=signature;
    const forecast=this._forecastPlan(),list=this.$('forecast-list');
    list.replaceChildren();
    list.hidden=!forecast.items.length;
    this.$('forecast-standard').hidden=forecast.standard===undefined;
    this.$('forecast-standard').textContent=forecast.standard===null?this._t('standard_unavailable'):forecast.standard===undefined?'':this._t('assuming_amount',{amount:forecast.standard});
    this.$('forecast-note').classList.toggle('is-overdue',Boolean(forecast.overdue));
    if(forecast.status==='no-anchor'){
      this.$('forecast-context').textContent=this._t('forecast_no_anchor_context');
      this.$('forecast-note').textContent=this._t('forecast_no_anchor_note');
      return;
    }
    if(forecast.status==='no-deadline'){
      this.$('forecast-context').textContent=this._t('forecast_no_deadline_context');
      this.$('forecast-note').textContent=this._t('forecast_no_deadline_note');
      return;
    }
    this.$('forecast-context').textContent=this._t('forecast_range',{from:this._forecastDayLabel(forecast.anchor)+' '+this._parts(forecast.anchor*1000).time,to:this._forecastDayLabel(forecast.end)+' '+this._parts(forecast.end*1000).time});
    forecast.items.forEach((item,index)=>{
      const row=document.createElement('li');row.className='forecast-item';row.dataset.epoch=String(item.epoch);
      if(index===0){row.classList.add('is-next');row.classList.toggle('is-overdue',forecast.overdue);row.setAttribute('aria-current','step');}
      const dot=document.createElement('span');dot.className='forecast-dot';dot.setAttribute('aria-hidden','true');row.append(dot);
      const body=document.createElement('div');body.className='forecast-body';
      const appendText=({className,value})=>{const element=document.createElement('span');element.className=className;element.textContent=value;body.append(element);};
      appendText({className:'forecast-marker',value:this._t(index===0?(forecast.overdue?'marker_next_overdue':'marker_next'):'marker_expected')});
      appendText({className:'forecast-day',value:this._forecastDayLabel(item.epoch)});
      appendText({className:'forecast-time',value:this._parts(item.epoch*1000).time});
      appendText({className:'forecast-amount',value:item.cc===null?this._t('amount_not_set'):this._t('amount_value',{amount:item.cc})});
      appendText({className:'forecast-spacing',value:this._t('after_hours',{hours:item.intervalHours.toLocaleString(this._locale(),{maximumFractionDigits:2})})});
      row.append(body);list.append(row);
    });
    this.$('forecast-note').textContent=this._t(forecast.overdue?'forecast_note_overdue':forecast.items.length?'forecast_note_expected':'forecast_note_outside');
  }
  _tick(){if(!this._hass)return;const anchorParts=(this._state('plan_anchor')||'').split('|');const anchor=Number(anchorParts[1]);const raw=this._state('reminder')||'';let deadline=Number(raw);if(!(deadline>0)&&(raw==='alerted'||raw.startsWith('alerted:'))){const claimed=Number(raw.split(':')[1]),stored=Number(anchorParts[2]);deadline=claimed>0?claimed:stored>0?stored:anchor>0?anchor+this._interval(anchor)*3600:0;}const valid=Number.isFinite(deadline)&&deadline>0;const seconds=valid?Math.max(0,Math.ceil(deadline-Date.now()/1000)):0;const pad=value=>String(value).padStart(2,'0');this.$('countdown').textContent=valid?(seconds>0?`${pad(Math.floor(seconds/3600))}:${pad(Math.floor(seconds/60)%60)}:${pad(seconds%60)}`:this._t('time_for_bottle')):this._t('nothing_planned');this.$('deadline').hidden=!valid;this.$('deadline').textContent=valid?this._t('at_time',{time:this._parts(deadline*1000).time}):'';this.$('last-feed').textContent=anchor>0?this._t(anchor>Date.now()/1000?'bottle_at':'last_bottle',{time:this._parts(anchor*1000).time}):this._t('first_bottle');const span=valid&&anchor>0&&deadline>anchor?deadline-anchor:10800;this.$('progress').style.width=(valid?Math.max(0,Math.min(100,(1-seconds/span)*100)):0)+'%';this._patchForecast();}
  _patchCurrent(){if(!this._draft)return;this._preview('current-preview',this._draft);}
  _isAnchor(row){const anchor=(this._state('plan_anchor')||'').split('|');return Boolean(row)&&row.description===anchor[0]&&Date.parse(row.start)/1000===Number(anchor[1]);}
  _duration(seconds){const minutes=Math.ceil(seconds/60),hours=Math.floor(minutes/60),rest=minutes%60;return [hours?this._t('duration_hours',{n:hours}):'',rest||!hours?this._t('duration_minutes',{n:rest}):''].filter(Boolean).join(' ');}
  _preview(id,model){if(model.original&&!this._isAnchor(model.original)){this.$(id).textContent=this._t('history_preview');return;}try{const epoch=this._localEpoch(model.day,model.time,model.original?Date.parse(model.original.start):undefined),ahead=epoch-Date.now()/1000;if(ahead>0&&model.original===null){this.$(id).textContent=this._t('earlier_feed_future');return;}if(ahead>86400){this.$(id).textContent=this._t('more_than_24');return;}const hours=this._interval(epoch),next=this._parts((epoch+hours*3600)*1000);this.$(id).textContent=(ahead>0?this._t('ahead_prefix',{duration:this._duration(ahead)}):'')+this._t('next_reminder',{time:next.time,day:next.day!==model.day?this._t('on_day',{date:next.day.split('-').reverse().join('-')}):'',hours});}catch{this.$(id).textContent=this._t('rhythm_from_entered',{rhythm:this._rhythmSummary()});}}
  _updateSteps(){for(const prefix of ['current','edit']){const input=this.$(prefix+'-amount');for(const suffix of ['minus','plus']){const button=this.shadowRoot.querySelector(`[data-action="${prefix}-${suffix}"]`);button.disabled=this._busy||(suffix==='minus'?Number(input.value)<=0:Number(input.value)>=9999);}}}
  _onInput(event){const id=event.target.id,value=event.target.value;if(id.startsWith('current-')&&this._draft){if(id==='current-date'){this._draft.day=value;this._draft.dirtyTime=true;}if(id==='current-time'){this._draft.time=value;this._draft.dirtyTime=true;}if(id==='current-amount'){this._draft.amount=value;this._draft.dirtyAmount=value!==this._draft.baselineAmount;}this._error('current-error','');this._patchCurrent();this._updateSteps();}if(id.startsWith('edit-')&&this._editor){if(id==='edit-date')this._editor.day=value;if(id==='edit-time')this._editor.time=value;if(id==='edit-amount')this._editor.amount=value;this._error('edit-error','');this._preview('edit-preview',this._editor);this._updateSteps();}if(['standard-amount','maximum-amount','night-hours'].includes(id)){if(id==='night-hours'){if(this._nightDraft)this._nightDraft.hours=value;this._nightDirty=true;}else this._settingsDirty=true;this.$('settings-status').textContent=this._t('not_saved_yet');this._error('settings-error','');this._patchNightSettings();}}
  _path(){const path=this._mode==='timer'?this._config?.navigation_path:'';return typeof path==='string'&&/^\/(?!\/)/.test(path)?path:'';}
  _open(){const path=this._path();if(!path)return;history.pushState(null,'',path);window.dispatchEvent(new CustomEvent('location-changed',{bubbles:true,composed:true,detail:{replace:false}}));}
  _onClick(event){if(this._mode==='timer'){if(event.target.closest('.timer'))this._open();return;}const target=event.target.closest('button');if(!target)return;const action=target.dataset.action;if(!action)return;event.stopPropagation();if(action.startsWith('mode-')){this._mode=action.slice(5);this._renderMode();if(this._mode==='history')this._scheduleRefresh();return;}if(action==='today'){this._changeDay(this._parts(Date.now()).day);return;}if(action==='refresh'){this._refreshAll();return;}if(action==='new'){this._startNew(false);return;}if(action==='recover'){this._startNew(true);return;}if(action==='add-history'){this._openHistory(null);return;}if(action==='cancel-edit'){this._editor=null;this.$('history-editor').hidden=true;return;}if(action==='edit-row'){this._openHistory(this._dayRows[Number(target.dataset.index)]);return;}if(action==='night-toggle'){const saved=this._nightPolicy();this._nightDraft=this._nightDraft||{active:saved.active,hours:String(saved.selectedHours)};this._nightDraft.active=!this._nightDraft.active;this._nightDirty=true;this.$('settings-status').textContent=this._t('not_saved_yet');this._error('settings-error','');this._patchNightSettings();return;}if(action==='standard-plus'){const next=Number(this.$('standard-amount').value)+10,max=Number(this.$('maximum-amount').value);if(next>9999||max>0&&next>max){this._error('settings-error',this._t('step_above_max'));return;}this.$('standard-amount').value=String(next);this._settingsDirty=true;this.$('settings-status').textContent=this._t('not_saved_yet');return;}const match=action.match(/^(current|edit)-(minus|plus)$/);if(match){const prefix=match[1],value=Math.max(0,Math.min(9999,Number(this.$(prefix+'-amount').value)+(match[2]==='plus'?1:-1)));this.$(prefix+'-amount').value=String(value);this._onInput({target:this.$(prefix+'-amount')});}}
  _error(id,message){this.$(id).textContent=message;this.$(id).hidden=!message;}
  _show(message,error=false){this._notice=message;this._noticeError=error;this._patch();}
  _message(error){if(error?.translation_key&&BABY_FEEDING_TEXT.en['error_'+error.translation_key])return this._t('error_'+error.translation_key);const text=error?.message||String(error||'');return /not found|unauthorized|forbidden|fetch|network|websocket|connection/i.test(text)?this._t('connection_lost'):text||this._t('generic_failure');}
  async _call(domain,service,data,response=true){return this._hass.callWS({type:'call_service',domain,service,service_data:data,return_response:response});}
  async _freshStates(){const rows=await this._hass.callWS({type:'get_states'});const states=Object.fromEntries(rows.map(row=>[row.entity_id,row]));this._hass={...this._hass,states};this._syncFields();this._patch();return states;}
  async _startNew(recover){if(this._busy)return;this._busy=true;this._patch();try{await this._call('baby_feeding','new_bottle',{});await this._freshStates();const stored=this._number('saved_marker',0)>0;if(!(Number(this._draft?.session)>0)||!recover&&stored)throw Error(this._t('new_not_confirmed'));this._show(this._t(recover?(stored?'restored_saved':'restored_open'):'new_bottle_ready'));}catch(error){this._show(this._message(error),true);}finally{this._busy=false;this._patch();}}
  async _saveCurrent(){if(this._busy||!this._draft||this._number('saved_marker',0)>0)return;let snapshot;try{snapshot={...this._draft,day:this.$('current-date').value,time:this.$('current-time').value,cc:this._validAmount(this.$('current-amount').value),start:this._validMoment(this.$('current-date').value,this.$('current-time').value)};}catch(error){this._error('current-error',this._message(error));return;}this._busy=true;this._patch();this._error('current-error','');try{const result=await this._call('baby_feeding','save_bottle',{start:new Date(snapshot.start*1000).toISOString(),amount:snapshot.cc});let confirmed=Boolean(result?.response?.plan_feed_id);if(!confirmed)confirmed=await this._verifyNew(snapshot);if(!confirmed)throw Error(this._t('save_not_confirmed'));this._draft.confirmedAmount=snapshot.cc;await this._freshStates();await this._refreshAll();this._show(this._t('saved_notice',{time:snapshot.time,amount:snapshot.cc}));}catch(error){let confirmed=false;if(error?.code!=='service_validation_error'){try{confirmed=await this._verifyNew(snapshot);}catch{}}if(confirmed){this._draft.confirmedAmount=snapshot.cc;await this._freshStates();await this._refreshAll();this._show(this._t('saved_notice',{time:snapshot.time,amount:snapshot.cc}));}else{this._error('current-error',this._message(error));this._show(this._message(error),true);}}finally{this._busy=false;this._patch();}}
  async _verifyNew(snapshot){const rows=await this._eventsForDay(snapshot.day);return rows.some(row=>row.cc===snapshot.cc&&Math.floor(Date.parse(row.start)/1000)===snapshot.start);}
  _range(day){const midnight=Date.parse(day+'T00:00:00Z');return {start:new Date(midnight-12*3600000).toISOString(),end:new Date(midnight+36*3600000).toISOString()};}
  _mapEvents(events){return events.filter(event=>/^\s*\d+\s*(cc|ml)\s*$/i.test(event.summary||'')).map(event=>{const start=event.start?.dateTime,end=event.end?.dateTime,stamp=Date.parse(start);if(!Number.isFinite(stamp)||!event.uid)return null;const p=this._parts(stamp);return {uid:event.uid,description:event.description||event.uid,summary:event.summary,start,end,cc:Number(event.summary.match(/\d+/)[0]),day:p.day,time:p.time};}).filter(Boolean);}
  async _query(start,end){const params=new URLSearchParams({start,end});return this._mapEvents(await this._hass.callApi('GET','calendars/calendar.baby_feeding_diary?'+params));}
  async _eventsForDay(day){const range=this._range(day);return (await this._query(range.start,range.end)).filter(row=>row.day===day);}
  async _refreshAll(){if(!this._hass||this._mode==='timer')return;const sequence=++this._refreshSequence;this.$('history-loading').hidden=false;this._error('history-error','');const selected=this._selectedDay||this._parts(Date.now()).day;const today=this._parts(Date.now()).day;const utc=new Date(today+'T12:00:00Z');utc.setUTCDate(utc.getUTCDate()-(utc.getUTCDay()+6)%7);const monday=utc.toISOString().slice(0,10),range=this._range(monday),end=this._range(today).end;const result=await Promise.allSettled([this._eventsForDay(selected),this._query(range.start,end)]);if(sequence!==this._refreshSequence)return;if(result[0].status==='fulfilled'){this._dayRows=result[0].value.sort((a,b)=>Date.parse(b.start)-Date.parse(a.start));this._dayLoaded=true;this._renderRows();}else this._error('history-error',this._t('load_failed'));if(result[1].status==='fulfilled'){this._weekRows=result[1].value.filter(row=>row.day>=monday&&row.day<=today);this._weekLoaded=true;this._patchStats();}this.$('history-loading').hidden=true;this._patch();}
  _patchStats(){if(!this._weekLoaded)return;const today=this._parts(Date.now()).day,rows=this._weekRows.filter(row=>row.day===today);const sum=list=>list.reduce((total,row)=>total+row.cc,0),daily=sum(rows),weekly=sum(this._weekRows),days=new Set(this._weekRows.map(row=>row.day)).size,format=value=>value.toLocaleString(this._locale(),{maximumFractionDigits:1});this.$('today-total').textContent=this._t('amount_value',{amount:daily});this.$('week-total').textContent=this._t('amount_value',{amount:weekly});this.$('today-average').textContent=this._t('today_average',{count:rows.length,avg:format(rows.length?daily/rows.length:0)});this.$('week-average').textContent=this._t('week_average',{avg:format(days?weekly/days:0),days});}
  _renderRows(){const list=this.$('history-list');list.replaceChildren();this._dayRows.forEach((row,index)=>{const button=document.createElement('button');button.type='button';button.className='row';button.dataset.action='edit-row';button.dataset.index=String(index);button.setAttribute('aria-label',this._t('edit_row_aria',{day:row.day,time:row.time,amount:row.cc}));button.setAttribute('aria-expanded',this._editor?.original?.uid===row.uid?'true':'false');for(const [className,value]of[['row-time',row.time],['row-cc',this._t('amount_value',{amount:row.cc})],['row-change',this._t('edit_button')]]){const span=document.createElement('span');span.className=className;span.textContent=value;button.append(span);}list.append(button);});this.$('history-empty').hidden=!this._dayLoaded||this._dayRows.length>0;const day=this._selectedDay;this.$('history-title').textContent=day===this._parts(Date.now()).day?this._t('saved_today'):new Date(day+'T12:00:00Z').toLocaleDateString(this._locale(),{timeZone:this._zone(),weekday:'long',day:'numeric',month:'long'});}
  _changeDay(day){if(!/^\d{4}-\d{2}-\d{2}$/.test(day)||day>this._tomorrow()){this._error('history-error',this._t('choose_day'));return;}if(this._busy)return;this._selectedDay=day;this.$('history-day').value=day;this._editor=null;this.$('history-editor').hidden=true;this._dayLoaded=false;this._dayRows=[];this._renderRows();this._refreshAll();}
  _openHistory(row){if(this._busy)return;this._mode='history';this._renderMode();const now=this._parts(Date.now());this._editor=row?{original:{...row},day:row.day,time:row.time,amount:String(row.cc)}:{original:null,day:this._selectedDay||now.day,time:now.time,amount:String(this._number('standard_amount',20))};for(const [id,key]of[['edit-date','day'],['edit-time','time'],['edit-amount','amount']])this.$(id).value=this._editor[key];this.$('history-editor').hidden=false;this.$('editor-heading').textContent=this._t(row?'edit_feed':'add_earlier_feed');this._error('edit-error','');this._preview('edit-preview',this._editor);this._updateSteps();this.$('history-editor').scrollIntoView({behavior:'smooth',block:'nearest'});}
  async _saveHistory(){if(this._busy||!this._editor)return;const model={...this._editor,day:this.$('edit-date').value,time:this.$('edit-time').value,amount:this.$('edit-amount').value};let start,cc;try{cc=this._validAmount(this.$('edit-amount').value);const unchanged=model.original&&model.day===model.original.day&&model.time===model.original.time;start=unchanged?Date.parse(model.original.start)/1000:this._validMoment(this.$('edit-date').value,this.$('edit-time').value);if(!unchanged&&start>Date.now()/1000&&!this._isAnchor(model.original))throw Error(this._t(model.original?'only_planned_ahead':'earlier_feed_future'));}catch(error){this._error('edit-error',this._message(error));return;}this._busy=true;this._patch();let written=false;try{if(!model.original){await this._call('baby_feeding','add_earlier_feed',{start:new Date(start*1000).toISOString(),amount:cc});written=true;}else{const rows=await this._eventsForDay(model.original.day),existing=rows.find(row=>row.uid===model.original.uid);if(!existing)throw Error(this._t('feed_moved'));if(existing.summary!==model.original.summary||Date.parse(existing.start)!==Date.parse(model.original.start))throw Error(this._t('feed_changed_elsewhere'));const sameMoment=model.day===model.original.day&&model.time===model.original.time;await this._call('baby_feeding','update_feed',{feed_id:existing.uid,start:sameMoment?model.original.start:new Date(start*1000).toISOString(),amount:cc});written=true;}this._editor=null;this.$('history-editor').hidden=true;this._selectedDay=model.day;this.$('history-day').value=model.day;await this._freshStates();await this._refreshAll();this._show(this._t('saved_notice',{time:model.time,amount:cc}));}catch(error){if(written){this._editor=null;this.$('history-editor').hidden=true;await this._refreshAll();this._show(this._t('saved_overview_updating'));}else this._error('edit-error',this._message(error));}finally{this._busy=false;this._patch();}}
  async _saveSettings(){
    if(this._busy)return;
    let amount,max,night,amountChanged,nightChanged;
    try{
      amount=this._validAmount(this.$('standard-amount').value);
      const raw=this.$('maximum-amount').value.trim();max=raw?this._validAmount(raw):null;
      if(max!==null&&max<1)throw Error(this._t('maximum_too_low'));
      if(max!==null&&amount>max)throw Error(this._t('standard_above_maximum'));
      const rawHours=this.$('night-hours').value.trim(),hours=Number(rawHours);
      if(!rawHours||!Number.isInteger(hours)||hours<3||hours>8)throw Error(this._t('night_hours_invalid'));
      const savedNight=this._nightPolicy();night={active:this._nightDraft?.active??savedNight.active,hours};
      amountChanged=amount!==this._number('standard_amount',20)||(this._state('maximum_amount')||'')!==(max===null?'':String(max));
      nightChanged=this._nightDirty||night.active!==savedNight.active||night.hours!==savedNight.selectedHours;
    }catch(error){this._error('settings-error',this._message(error));return;}
    this._settingsDirty=this._settingsDirty||amountChanged;this._nightDirty=this._nightDirty||nightChanged;this._busy=true;this._patch();
    try{
      if(amountChanged||nightChanged)await this._call('baby_feeding','set_settings',{standard_amount:amount,maximum_amount:max,night_custom_enabled:night.active,night_hours:night.hours});
      const saved=(await this._freshStates())['sensor.baby_feeding_status']?.attributes||{};
      const nightConfirmed=saved.night_custom_enabled===night.active&&saved.night_hours===night.hours;
      const amountConfirmed=saved.standard_amount===amount&&(saved.maximum_amount??null)===max;
      if(!nightConfirmed||!amountConfirmed)throw Error(this._t('settings_not_confirmed'));
      this._settingsDirty=false;this._nightDirty=false;this._syncFields();
      this.$('settings-status').textContent=this._t('settings_saved');this._error('settings-error','');
      this._show(this._t('settings_saved_notice'));
    }catch(error){this._error('settings-error',this._message(error));}
    finally{this._busy=false;this._patch();}
  }
  _scheduleRefresh(){if(!this.isConnected||!this._hass)return;clearTimeout(this._refreshTimeout);this._refreshTimeout=setTimeout(()=>this._refreshAll(),180);}
  _subscribe(){}
}
if(!customElements.get('baby-feeding-card'))customElements.define('baby-feeding-card',BabyFeedingCard);
window.customCards=window.customCards||[];window.customCards.push({type:'baby-feeding-card',name:'Voedingsdagboek',preview:false,description:'Flesvoeding, geschiedenis en herinneringen.'});
