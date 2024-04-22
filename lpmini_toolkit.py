# Functions related to using the launchpad mini.
import lpminimk3 as mk3
import json
#from visca_toolkit import visca_tcp_recall_preset
#import ndi_toolkit as ndi
#import obs_toolkit as obs


def init_matrix(config):
    # build the initial matrix from the config.
    # Set everything to off initially.

    # Some color notation shorthand
    X=0; W=1; R=5; B=51; G=25;
    
    # Initialize the matrix
    matrix = [
        [X,X,X,X,X,X,X,X,X],
        [X,X,X,X,X,X,X,X,X],
        [X,X,X,X,X,X,X,X,X],
        [X,X,X,X,X,X,X,X,X],
        [X,X,X,X,X,X,X,X,X],
        [X,X,X,X,X,X,X,X,X],
        [X,X,X,X,X,X,X,X,X],
        [X,X,X,X,X,X,X,X,X],
        [X,X,X,X,X,X,X,X,X],
    ]

    matrix[0]=[X,X,X,X,X,X,X,X,W]  # Set the control row.

    # Add configured cameras to the initial matrix.
    for item in config:

        if item['action']=="play":
            matrix[item['row']][item['col']]=W

        if item['action']=="playlist-start":
            matrix[item['row']][item['col']]=W
        if item['action']=="playlist-next":
            matrix[item['row']][item['col']]=W
        if item['action']=="playlist-prev":
            matrix[item['row']][item['col']]=W

        if item['action']=="stop":
            matrix[item['row']][item['col']]=R

    return matrix


# Set the launchpad button colors for scene / position change actions.
def lp_set_active_view(cam,view_index,mtx):
    #print("preset selected!")

    # Set all preset selectors white
    for i in range(len(cam['views'])):
        mtx[cam['row']][i]=1
    
    # Turn the selected preset green
    mtx[cam['row']][view_index]=25

    # If camera supports NDI, prioritize that.
    if (cam.get('ptz_controls')=="NDI"):
        if (cam.get("ndi_recv")):
            print(f"NDI Control - Preset recall on {cam['ndi_name']}:  Preset ", end="")
            print(ndi.recall_preset(cam['ndi_recv'],view_index))

    elif (cam.get('ptz_controls')=="VISCA_TCP"):
        print(f"VISCA TCP Controls configured for cam at {cam.get['ip_address']}")
        visca_tcp_recall_preset(cam['ip_address'], cam['visca_port'],view_index)

    mtx[8][8]=0

    return mtx


# Set the launchpad button colors for a source select action.
def lp_set_program_source(cam,mtx,config):
    #print("lp_set_program_source")
    x=8
    y=cam['row']

    # Turn all source lights white.
    all_sources = get_all_source_rows(config)
    for source in all_sources:
        mtx[source][8]=1

    # Turn the selected source light on.
    mtx[y][x]=25

    return mtx


def btn_is_bso_modifier(coord,config):
    if coord[1]==config['bso_util']['row']:
        return True
    return False

def btn_is_scoreboard_modifier(coord,config):
    if (coord[1])==config['score_util']['row'] and coord[0] != 8:
        return True
    return False

def btn_is_ptz_modifier(coord):
    if (coord[1]==0):
        return True
    return False

# Checks for NDI PTZ support.
def cam_supports_ptz(cam):
    if cam is None:
        return False
    
    if cam.get('ptz_capable'):
        return cam['ptz_capable']
    
    return False

# When buttons are pressed or released, handle them here.
def handle_lp_event(btn_event,mtx,scoreboard,config):
    #print("handle_lp_event")
    
    if btn_event and btn_event.type=="press":  # Button was pressed.

        x = btn_event.button.x
        y = btn_event.button.y

        ################################################
        # Handle the cam view selector buttons.
        # These can trigger a scene change or a PTZ camera move.
        if (btn_is_view_selector([x,y],config)):
            cam = get_cam_from_row(y,config)
            mtx = lp_set_active_view(cam,x,mtx)

            # If the view change affects the active program, do it now.
            if (mtx[y][8]==25):
                print("View change called on active scene.   Sending to preview.")
                obs.set_preview_scene(cam['views'][x])

            else:
                print("View change called on a non-program scene.   Sending to preview.")
                obs.set_preview_scene(cam['views'][x])
                
            # This tracks the camera that was last used, not the camera on the program screen.
            # Used for setting PTZ controls etc to the last button pressed.
            # Needed for positioning PTZ and saving pre-sets in the preview window.
            config['active_camera']=cam


        #################################################
        # If button is a source change selector
        if (btn_is_program_selector([x,y],config)):
            #print("Button is program selector!")
            cam = get_cam_from_row(y,config)
            mtx = lp_set_program_source(cam,mtx,config)
            
            # Inform OBS to use the selected view.
            view = get_active_view(cam,mtx)
            obs.set_program_scene(view)

        ##########################################
        # If button is a BSO modifier
        if (btn_is_bso_modifier([x,y],config)):
            if x==0 or x==1 or x==2:   # ball
                balls=x+1
                if scoreboard['balls']==balls:
                    balls=0
                scoreboard['balls']=balls

            if x==3 or x==4: # strike
                strikes=(x-2)
                if scoreboard['strikes']==strikes:
                    strikes=0
                scoreboard['strikes']=strikes
            
            if x==5 or x==6: # outs
                outs=(x-4)
                if scoreboard['outs']==outs:
                    outs=0
                scoreboard['outs']=outs
            
            print("Scoreboard updated: ", json.dumps(scoreboard,indent=2))

        ##########################################
        # If button is a scoreboard modifier
        if (btn_is_scoreboard_modifier([x,y],config)):
            btn_event.button.led.color=119
            if x==0: scoreboard['home']-=1
            if x==1: scoreboard['home']+=1
            if x==2: scoreboard['away']-=1
            if x==3: scoreboard['away']+=1
            if x==5: scoreboard['inning']-=1
            if x==6: scoreboard['inning']+=1
            if x==7: scoreboard['bottom'] = not scoreboard['bottom']

            print("Scoreboard updated: ", json.dumps(scoreboard,indent=2))

        
            
        if (btn_is_ptz_modifier([x,y]) or (x==8 and y==8)):
            if (cam_supports_ptz(config['active_camera'])):
                recv=config['active_camera']['ndi_recv']
                if x==0: # Tilt up
                    ndi.pan_tilt_speed(recv,0,0.2)
                if x==1: # Tilt down
                    ndi.pan_tilt_speed(recv,0,-0.2)
                if x==2: # Tilt left
                    ndi.pan_tilt_speed(recv,0.2,0)
                if x==3: # Tilt right
                    ndi.pan_tilt_speed(recv,-0.2,0)
                if x==4: #zoom in
                    ndi.zoom_speed(recv, 0.2)
                if x==5: #zoom out
                    ndi.zoom_speed(recv, -0.2)
                if x==6: #focus in
                    ndi.focus_speed(recv, 0.2)
                if x==7 and y==0: #focus out
                    ndi.focus_speed(recv, -0.2)
                if x==8 and y==8 and mtx[8][8]==5: # Save preset if "armed"
                    print("Saving preset!")
                    row=config['active_camera']['row']
                    preset_pos=-1
                    for i in range(len(config['active_camera']['views'])):
                        if mtx[row][i]!=1:
                            preset_pos=i

                    if (preset_pos >=0 and preset_pos < 8): # seems valid, try to save it.
                        print("preset pos: ",preset_pos)
                        ndi.store_preset(recv,preset_pos)
                        mtx[8][8]=0
                        cam_row = config['active_camera']['row']
                        cam_col = get_active_view_index(config['active_camera'],mtx)
                        mtx[cam_row][cam_col]=25
    
    if btn_event and btn_event.type=="release":  # Button was released.
        x = btn_event.button.x
        y = btn_event.button.y
    
        if (btn_is_ptz_modifier([x,y])):
            if (cam_supports_ptz(config['active_camera'])):
                recv=config['active_camera']['ndi_recv']
                if x==0: # Tilt up
                    ndi.pan_tilt_speed(recv,0,0)
                if x==1: # Tilt down
                    ndi.pan_tilt_speed(recv,0,0)
                if x==2: # Tilt left
                    ndi.pan_tilt_speed(recv,0,0)
                if x==3: # Tilt right
                    ndi.pan_tilt_speed(recv,0,0)
                if x==4: #zoom in
                    ndi.zoom_speed(recv, 0)
                if x==5: #zoom out
                    ndi.zoom_speed(recv, 0)
                if x==6: #focus in
                    ndi.focus_speed(recv, 0)
                if x==7 and y==0: #focus out
                    ndi.focus_speed(recv, 0)
                
                # If a modifier is released, light up the save preset button.
                mtx[8][8]=5
                mod_row = config['active_camera']['row']
                mod_col = get_active_view_index(config['active_camera'],mtx)
                mtx[mod_row][mod_col]=5 # turn the modified preset red for the moment.

                #print(mtx)
                

    return mtx

def render_scoreboard_util(mtx,scoreboard,config):

    sb_row = mtx[config['score_util']['row']]
    sb_row[0] = config['score_util']['home'][1]
    sb_row[1] = config['score_util']['home'][0]
    sb_row[2] = config['score_util']['away'][1]
    sb_row[3] = config['score_util']['away'][0]
    sb_row[4] = 0  # blank
    sb_row[5] = config['score_util']['inning'][1]
    sb_row[6] = config['score_util']['inning'][0]

    if scoreboard['bottom']==True:
        sb_row[7] = config['score_util']['top_bottom'][1]
    else:
       sb_row[7] = config['score_util']['top_bottom'][0]

    #sb_row.append(0)

    mtx[config['score_util']['row']]=sb_row

    return mtx

def render_bso_util(mtx,scoreboard,config):
    #print("render_bso_util")
    bso_row = []

    # How many balls are there?
    for b in range(3):
        if scoreboard['balls'] > b:
            bso_row.append(config['bso_util']['ball'][1])
        else:
            bso_row.append(config['bso_util']['ball'][0])
        
    for s in range(2):
        if scoreboard['strikes'] > s:
            bso_row.append(config['bso_util']['strike'][1])
        else:
            bso_row.append(config['bso_util']['strike'][0])

    for o in range(2):
        if scoreboard['outs'] > o:
            bso_row.append(config['bso_util']['out'][1])
        else:
            bso_row.append(config['bso_util']['out'][0])

    bso_row.append(0)
    bso_row.append(0)

    mtx[config['bso_util']['row']]=bso_row
    return mtx


def init_launchpad():
    lp = mk3.find_launchpads()
    if (lp):
        lp=lp[0]
        lp.open()
        lp.mode = mk3.Mode.PROG
        return lp
    else:
        return False
    

    # Writes the matrix colors to launchpad if they don't match matrix_displayed.
def write_colors(lp,mtx):

    # Render the matrix colors as provided.
    for yidx, row in enumerate(mtx):
        for xidx, val in enumerate(row):
            lp.panel.led(x=xidx,y=yidx).color=val
    

# Sets all buttons to off.
def clear_panel(lp):
    for led in lp.panel.led_range():
        del led.color

def btn_is_view_selector(coord, config):
    for cam in config['cameras']:
        if cam['row']==coord[1] and len(cam['views'])>coord[0]:
            return True
    return False

def btn_is_program_selector(coord,config):
    if coord[0]==8 and coord[1] in get_all_source_rows(config):
        #print("This is a source selector!")
        return True
    return False

def get_cam_from_row(row, config):
    for cam in config['cameras']:
        if cam['row']==row:
            return cam
    return False

def get_all_source_rows(config):
    sources = []
    for cam in config['cameras']:
        sources.append(cam['row'])
    return sources

def get_active_view(cam,mtx):
    row = cam['row']
    for i in range(len(cam['views'])):
        if mtx[row][i]!=1:
            return cam['views'][i]
    return -1

def get_active_view_index(cam,mtx):
    row = cam['row']
    for i in range(len(cam['views'])):
        if mtx[row][i]!=1:
            return i
    return -1

