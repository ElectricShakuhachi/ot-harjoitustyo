import math
from copy import deepcopy
import config.shaku_constants as consts
from entities.shaku_note import ShakuNote

class ShakuRhythmNotation:
    def __init__(self, mode):
        if mode not in ["Tozan", "Kinko", "Ueda"]:
            raise ValueError(f"Notation system {mode} not supported")
        self.mode = mode

    def _create_arch(self, x_start, y_start, x_end, y_end, arch=10): # get arch steepness from config
        tangent = math.atan2(y_end - y_start, x_end - x_start)
        x_mid = (x_start + x_end)/2 + math.sin(tangent) * arch
        y_mid = (y_start + y_end)/2 - math.cos(tangent) * arch
        return (x_start, y_start, x_mid, y_mid, x_end, y_end) # MOVE THIS SOMEWHERE FOR COMMON USAGE
        # BECAUSE ITS GOING TO BE NEEDED TO ADD THE SPECIAL NOTATION = legato

    def _dotted(self, rhythm):
        if 4 < rhythm < 8 or 8 < rhythm < 16 or 16 < rhythm < 32:
            return True
        return False

    def _measure_rhytms(self, notes: list, positions: list): #BREAK THIS DOWN TO SUBFUNCTION FOR EACH CASE TYPE?
        lines = []
        total = sum([note.lenght for note in notes])
        limit = consts.MEASURE_LENGHT * 8
        if total > limit:
            last_note = notes[-1]
            if last_note.pitch >= 0:
                remainer = total - limit
                last_note.lenght -= remainer
                arch_start = positions[-1][1] + 2
                arch_end = positions[0][1] + consts.NOTE_Y_SPACING * consts.MEASURE_LENGHT * 4 + consts.MEASURE_SKIP_LENGHT + 4
                arch_x = positions[-1][0] + 20 # get this from config as consts.NOTE_TO_ARCH_X_GAP (or smth)
                remainer_note = deepcopy(last_note)
                remainer_note.lenght = remainer
                ghost_pos = list(positions[-1])
                ghost_pos[1] = positions[0][1] + consts.MEASURE_LENGHT * 4 * consts.NOTE_Y_SPACING + consts.MEASURE_SKIP_LENGHT
                if ghost_pos[1] > consts.GRID_Y[1]:
                    ghost_pos[1] = consts.PARTS_Y_START
                lines.append((remainer_note, tuple(ghost_pos)))
                lines.append(self._create_arch(arch_x, arch_start, arch_x, arch_end))

        # get left note line for all 8th + 16th clusters
        clusters = []
        prev = None
        tmp = []
        for i in range(len(notes)):
            if notes[i].lenght < 8 and (prev is None or prev.lenght >= 8 or prev.pitch < 0) and notes[i].pitch >= 0: #cluster start if true
                tmp = [i]
            elif len(tmp) > 0 and (notes[i].lenght >= 8 or notes[i].pitch < 0): #cluster ends on previous if true
                tmp.append(i - 1)
                clusters.append(tmp)
                tmp = []
            prev = notes[i]

        if len(tmp) > 0: #if cluster continues until measure end - last one is another cluster end
            tmp.append(i)
            clusters.append(tmp)
        for cluster in clusters:
            line_x = positions[cluster[0]][0] + consts.NOTE_TO_RHYTM_SPACING
            y_start = positions[cluster[0]][1]
            y_end = positions[cluster[-1]][1] + 10
            lines.append((line_x, y_start, line_x, y_end))
            if cluster[0] == cluster[1] and 4 <= notes[cluster[0]].lenght < 8: # lonesom 8th note needs a dot
                i = cluster[0]
                x_start = positions[i][0] + consts.NOTE_TO_RHYTM_SPACING - 1
                x_end = x_start + 5
                y_start = positions[i][1] + 4
                y_end = y_start + 4 # CONSIDER GETTING THESE FROM CONFIG TOO
                lines.append((x_start, y_start, x_end, y_end))

        # get right note line for all 16th clusters (obviously going to make a function working for both cluster cases)
        # get left note line for all 8th + 16th clusters
        clusters = []
        prev = None
        tmp = []
        for i in range(len(notes)):
            if notes[i].lenght < 4 and (prev is None or prev >= 4):
                tmp = [i]
            elif len(tmp) > 0 and notes[i].lenght >= 4:
                tmp.append(i - 1)
                clusters.append(tmp)
                tmp = []
            prev = notes[i].lenght
        if len(tmp) > 0:
            tmp.append(i)
            clusters.append(tmp)
        for cluster in clusters:
            line_x = positions[cluster[0]][0] + consts.NOTE_TO_RHYTM_SPACING + consts.RHYTM_LINE2_TO_LINE1_SPACING
            y_start = positions[cluster[0]][1]
            y_end = positions[cluster[-1]][1] + 10
            lines.append((line_x, y_start, line_x, y_end))

        #notation for fourth notes and dotted notes
        for i in range(len(notes)):
            #fourths
            if notes[i].lenght >= 8 and notes[i].lenght < 16 and notes[i].pitch >= 0:
                line_x = positions[i][0] + consts.NOTE_TO_RHYTM_SPACING
                y_start = positions[i][1]
                y_end = positions[i][1] + 10
                lines.append((line_x, y_start, line_x, y_end))

            # dotted (in terms of lenght)
            if self._dotted(notes[i].lenght):
                line_x = positions[i][0] + 10
                start_y = positions[i][1] + 10
                end_y = start_y + 10 # CONSIDER MAKING DIFFERENT const.UNDER_NOTE_LINE_SIZE
                lines.append((line_x, start_y, line_x, end_y))

        return lines

    def tozan_rhytms(self, notes: list, positions: list):
        rhytm_notations = []
        measure_duration = consts.MEASURE_LENGHT * 8
        i = 0
        measure_notes = []
        measure_positions = []
        duration = 0

        while i < len(notes):
            while i < len(notes) and duration < measure_duration:
                duration += notes[i].lenght
                measure_notes.append(notes[i])
                measure_positions.append(positions[i])
                i += 1
            temp_posses = deepcopy(measure_positions)
            if len(measure_positions) > 1:
                temp_posses[0] = list(temp_posses[0])
                temp_posses[0][0] = temp_posses[1][0] 
                temp_posses[0] = tuple(temp_posses[0])
            notations = self._measure_rhytms(deepcopy(measure_notes), temp_posses)
            for notation in notations:
                rhytm_notations.append(notation)
            if len(notations) > 0 and isinstance(notations[0][0], ShakuNote):
                measure_notes = [notations[0][0]]
                ghost_pos = list(measure_positions[0])
                ghost_pos[1] += consts.MEASURE_LENGHT * 4 * consts.NOTE_Y_SPACING + consts.MEASURE_SKIP_LENGHT
                if ghost_pos[1] > consts.GRID_Y[1]:
                    ghost_pos[1] = consts.PARTS_Y_START
                measure_positions = [tuple(ghost_pos)]
                duration = notations[0][0].lenght
            else:
                measure_notes = []
                measure_positions = []
                duration = 0
        return rhytm_notations
