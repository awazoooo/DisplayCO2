# coding: UTF-8

import mh_z19

if __name__ == '__main__':
    # root authority required
    dat = mh_z19.read_all()
    with open('/root/DisplayCO2/co2_logs/log', 'w') as fp:
        fp.write('{0:d},{1:d}\n'.format(dat['temperature'], dat['co2']))
