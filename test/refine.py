
#### unit : mm


def get_poinst_from_txt(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        f.close()

    points = []

    for line in lines:
        line = line.replace('),', ')),')
        fpl = line.split('), ')

        for fp in fpl:
            fp = fp.replace('(', '')
            fp = fp.replace(')', '')
            p = fp.split(', ')
            px = float(p[0])
            py = float(p[1])
            points.append((px, py))

    return points



def refine(points):
    pl = []
    # round up 
    for point in points:
        p = (int(point[0]), int(point[1]))
        pl.append(p)
    
    print(pl)
    # smoothing
    



if __name__=='__main__':
    refine(get_poinst_from_txt('kk.txt'))