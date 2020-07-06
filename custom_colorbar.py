import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

def _create_rectangles(colors, width, height, gap, direction):
    ''' Draw rectangles, each with specified colors
    
    Inputs
    ------
    colors: a list of RGBA color code for the rectangles
    width: width of each rectangle
    height: height of each rectangle
    gap: gap between two rectangles
    direction: either 'horizontal' or 'vertical'
    
    Returns
    -------
    pc: a patch collection object, containing the color boxes drawn.
    x: x positions of the lower left corner of the boxes
    y: y positions of the lower left corner of the boxes
    '''
    # define coordinates of rectangles
    n = len(colors)
    if direction == 'horizontal':
        x = np.arange(0, n*(width+gap), width+gap)
        y = np.array([0]*n)
    elif direction == 'vertical':
        x = np.array([0]*n)
        y = np.arange(0, n*(height+gap), height+gap)
    else:
        raise ValueError('direction parameter should be either horizontal or vertical')
    # create rectangle patch collections   
    boxes = []
    for i in range(n):
        rect = Rectangle((x[i], y[i]), width, height, linewidth=0,edgecolor='b',facecolor=colors[i])
        boxes.append(rect)
    pc = PatchCollection(boxes, match_original=True)
    return pc,x,y

def _add_text(ax, text_list, x, y, fontsize, rotation):
    ''' Add text to axis ax
    
    Inputs
    ------
    ax: the ax object
    text_list: a list of text to add
    x: a list of x positions for the text
    y: a list of y positions for the text
    
    Returns
    -------
    ax: the ax object, after adding text
    '''
    if len(text_list) != len(x):
        raise ValueError('number of text_list does not match number of x')
    
    for i in range(len(text_list)):
        ax.text(x[i],y[i],text_list[i], fontsize=fontsize, rotation=rotation)
    return ax

def _determine_text_offset(direction, w, h):
    """Determine the offset for text
    
    Inputs
    ------
    direction: direction of the colorbar.
    w: width of each box
    h: height of each box
    
    Returns
    -------
    dx: offset in x direction
    dy: offset in y direction
    """
    if direction == 'vertical':
        dx = w*1.05
        dy = h/2
    elif direction == 'horizontal':
        dx = 0
        dy = -h*0.5
    return dx, dy

def _determine_figure_boundary(x,y,dx,dy,w,h,direction):
    """Determine the figure boundary and figure size
    """
    fig_len = (max(x[-1], y[-1]) + max(w,h))*1.1
    if direction == 'vertical':
        x_boundary = [-fig_len/2, fig_len/2]
        y_boundary = [0, y[-1]+dy+h]
    elif direction == 'horizontal':
        x_boundary = [0, x[-1]+dx+w]
        y_boundary = [-fig_len/2, fig_len/2]
    return x_boundary, y_boundary

def draw_colormap(df_colormap, ax,w, h, g, text_offset=None, direction='vertical', fontsize=10, rotation=0):
    """ Draw customized colormap
    
    Inputs
    ------
    df_colormap: pandas dataframe with two columns:
        ['color']: stores the RGBA color
        ['text']: stores the lable for that color
    ax: a matplotlib.pyplot axis object
    w: width of each color box
    h: height of each color box
    g: gap between two color boxes.
    text_offset: controls the relative position of the text. If it is None, the position is automatically determined.
    direction: either to plot the colorbar in 'vertical' direction, or 'horizontal' direction.
    fontsize: the font size of the text
    rotation: the rotation angle of the text.
    
    Returns
    -------
    ax: the ax object after drawing the colormap
    """
    # extract colors and text lists from df.
    colors = df_colormap['color']
    tlist = df_colormap['text']
    if len(colors)!=len(tlist):
        raise ValueError('number of colors does not match number of names')
    # create color boxes
    pc, x, y = _create_rectangles(colors, width=w, height=h, gap=g, direction=direction)
    ax.add_collection(pc)
    # add text
    if not text_offset:
        dx, dy = _determine_text_offset(direction, w, h)
    else:
        dx, dy = text_offset
    ax = _add_text(ax, tlist, x+dx, y+dy, fontsize, rotation)
    # determine the figure boudary
    x_boundary, y_boundary = _determine_figure_boundary(x,y,dx,dy,w,h,direction)
    ax.set_xlim(x_boundary)
    ax.set_ylim(y_boundary)
    ax.set_axis_off()
    return ax