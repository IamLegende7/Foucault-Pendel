import FreeSimpleGUI as sg
import math
from re import sub

def calculate(hours: float, latitude: float):
    delta_degrees = round((360 / 24) * math.sin(latitude) * hours, 1)
    return delta_degrees

def draw_pie_slice(window, center, radius, slice_angle):
        # circle
        window['canvas'].TKCanvas.create_oval(center[0] - radius, center[1] - radius,
                                            center[0] + radius, center[1] + radius)

        start_angle = 90
        end_angle = slice_angle * -1

        # slice
        window['canvas'].TKCanvas.create_arc(center[0] - radius, center[1] - radius,
                                            center[0] + radius, center[1] + radius,
                                            start=start_angle, extent=end_angle,
                                            fill='red', outline='red')

        # outline of the slice and the remaining circle
        window['canvas'].TKCanvas.create_arc(center[0] - radius, center[1] - radius,
                                            center[0] + radius, center[1] + radius,
                                            start=start_angle, extent=360,
                                            outline='black', style='arc', width=2)

        # labels
        for angle in range(0, 360, 5):
            radian = math.radians(360 - (angle - 90))
            label_x = center[0] + (radius + 15) * math.cos(radian)
            label_y = center[1] - (radius + 15) * math.sin(radian)
            color = 'black' if angle > slice_angle else 'red'
            if angle > 180:
                display_angle = str((360 - angle) * -1)
            else:
                display_angle = str(angle)
            if ((angle <= 90 or angle >= 270) and (angle % 10) == 0) or ((not (angle <= 90 or angle >= 270)) and ((angle % 15) == 0)):
                window['canvas'].TKCanvas.create_text(label_x, label_y, text=display_angle, fill=color)

def delete_pie_slice(window):
    window['canvas'].TKCanvas.delete('all')

def main():
    sg.theme('SystemDefaultForReal')

    degrees_list = [
        "52,3 (KW)",
        "52,5 (Berlin)",
        "51,5 (London)",
        "38,9 (Washington DC)",
        "55,8 (Moskau)",
        "39,9 (Peking)"
    ]

    layout = [
        [   
            sg.Column([
                [sg.Text('Foucault Rechner')],
                [sg.Text("Stunden: ")],
                [sg.Text("Breitengrad: ")],
                [sg.Text('Abweichung:')],
                [sg.Text('')],
                [sg.Text('')],
                [sg.Text('')],
                [sg.Text('')],
                [sg.Button('Berechnen!')]
            ]),
            sg.Column([
                [sg.Text('')],
                [sg.Input(key='-hoursInput-', size=(20, None))],
                [sg.Combo(degrees_list, key='-latitudeInput-', size=(20, None))],
                [sg.Text(key='-Output-')],
                [sg.Text('')],
                [sg.Text('')],
                [sg.Text('')],
                [sg.Text('')],
                [sg.Button('Abbruch')]
            ]),   
            sg.Column([
                [sg.Canvas(key='canvas', size=(250, 250))]
            ])
        ]
    ]

    window = sg.Window('Foucault-Pendel-Rechner v.0.4', layout, finalize=True)

    canvas_elem = window['canvas']
    canvas = canvas_elem.TKCanvas

    draw_pie_slice(window, center=(125, 125), radius=100, slice_angle=0)
    window['-hoursInput-'].update(str("0"))
    window['-latitudeInput-'].update(degrees_list[0])

    quit = False
    while not quit:
        event, values = window.read()
        error = False
        if values['-latitudeInput-'] == None:
            latitude = 0
        else:
            try:
                latitude = float(sub( "[^0-9\.]", "", str(values['-latitudeInput-'].replace(',', '.').strip()) ))
            except:
                latitude = 0
                error = True
                window['-Output-'].update('Error: lesen vom Breitengrad')
        if event == sg.WINDOW_CLOSED or event == 'Abbruch':
            quit = True
        elif event == 'Berechnen!':
            delta_degrees = float(calculate(float(str(values['-hoursInput-']).replace(',', '.').strip()), latitude))
            delete_pie_slice(window)
            draw_pie_slice(window, center=(125, 125), radius=100, slice_angle=delta_degrees)
            if not error:
                window['-Output-'].update(f'ca. {delta_degrees}°')
            else:
                error = False

main()

#hours = float(input("Stunden: "))
#latitude = float(input("Breitengrad: "))
#print(f"Das Pendel sollte eine abweichung von ca. {delta_degrees}° haben.")