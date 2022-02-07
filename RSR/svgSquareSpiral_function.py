import svgwrite
import math
import subprocess
from svgwrite import cm, mm
def double_square_spiral_fermat(dx=5,dyi=5,xg=5,yg=5,xorig=0,yorig=0,turn=11,swidth=2):
    '''
        Function to create Double Spiral Resonator with
        given dimensions
        The final vector file need to be import to inkscape
        to be convert to dxf or other needed format
        dx, dy : are the base lines on x and y
        xg , yg : stand for xgrow and ygrow
        xorig , yorig : to change the origin of the structure
        turn : to specify the number of turns
        swidth : the width of ech line
    '''
    sign_x=1
    sign_y=1
    vlines_a=[]
    vlines_b=[]
    lines_a=[]
    lines_b=[]
    fname_polylines='square_spiral_'+str(turn)+'turns_polylines.svg'
    fname_lines='square_spiral'+str(turn)+'_lines.svg'
    for i in range(turn):
        if(i==0):
            dy=0
        if(i==1):
            dy=dyi+yg
        ##to make the end of lines to correspond
        if(turn%2==0 and i==turn-1):
            print("last y element")
            dyfsign=math.copysign(1,dy)
            dy=dy+dyfsign*-1*yg+dyfsign*swidth/2
        if(turn%2==1 and i==turn-1):
            print("last x element")
            dxfsign=math.copysign(1,dx)
            dx=dx+dxfsign*-1*xg+dxfsign*swidth/2
        ##--------------------------------------

        #coordinates of each line---------------
        print("dx",dx+xorig,"dy",dy+yorig)
        
        ## for drawing -------------------------
        lines_a.append((dx+xorig,dy+yorig))
        lines_b.append((-dx+xorig,-dy+yorig))

        vlines_a.append([dx+xorig,dy+yorig])
        vlines_b.append([-dx+xorig,-dy+yorig])
        #---------------------------------------
            
    ##here the main processing===================
        if(i%2==1):
            sign_x=-1*sign_x
            dx=abs(dx)+xg
            dx=dx*sign_x
        if(i%2==0 and i>0):
            sign_y=-1*sign_y
            dy=abs(dy)+yg
            dy=dy*sign_y
    ##-----------------------------------------   
    print("line positive coordonates",lines_a)

    dwg = svgwrite.Drawing(fname_lines, profile='tiny')
    hlines = dwg.add(dwg.g(id='hlines', stroke='green'))
    hlines1 = dwg.add(dwg.g(id='hlines1', stroke='red'))

    for j in range(len(vlines_a)-1):
        hlines.add(dwg.line(start=((vlines_a[j][0])*mm, (vlines_a[j][1])*mm), end=((vlines_a[j+1][0])*mm, (vlines_a[j+1][1])*mm)))
        hlines1.add(dwg.line(start=((vlines_b[j][0])*mm, (vlines_b[j][1])*mm), end=((vlines_b[j+1][0])*mm, (vlines_b[j+1][1])*mm)))

    dwg.save()
    ##polyline making-----------------------------
    dwg_ = svgwrite.Drawing(fname_polylines, profile='full',size=('100%', '100%'))
    firstarm= dwg_.polyline(points=lines_a[:], stroke='black', stroke_width=swidth, fill='none')
    secondarm= dwg_.polyline(points=lines_b[:], stroke='red', stroke_width=swidth, fill='none')
    dwg_.add(firstarm)
    dwg_.add(secondarm)
    dwg_.save()
    return [fname_polylines,fname_lines]

   
##call the function with parameters
[fnamep,fnamel]=double_square_spiral_fermat(dx=5,dyi=5,xg=5,yg=5)
##Optional, fit the structures to the file dimensions
actions=' --actions="select-all:all;FitCanvasToSelection;FileSave;FileClose;" '
command='inkscape --batch-process'+actions
try:
    process_p = subprocess.run(command+str(fnamep), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process_l = subprocess.run(command+str(fnamel), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except:
    print("Error processing: check if inkcape is installed and available on path")