import struct
import numpy

IS_FLOAT = 83289021

hdr_desc = [('nrows',    'int32'),
	    ('ncols',    'int32'),
	    ('delta_t',  'float64'),
	    ('datasize', 'int32'),
	    ('type',     'int32'),
	    ('pad',      '(44,)int32')]

hdr_type = numpy.dtype(hdr_desc)


class TDD:
    def  __init__(self):
	self.delta_t = -1
	self.type    = -1
        return

    @staticmethod
    def new(delta_t, id_filename = 'LinkIndex'):

        tdd = TDD()

        try:
            f = open(id_filename, "r")
            hdr = numpy.fromfile(f, hdr_type, 1)
            row_type = numpy.dtype([('junk', 'int32'), ('data', '(%d,)int32' % (hdr['ncols'][0]-1))])
            rowdata = numpy.fromfile(f, row_type, 1)
            ids = list(rowdata[0][1])
            f.close()
        except:
            raise RuntimeError("unable to load id_filename: %s" % id_filename)


        tdd.delta_t = delta_t
        tdd.ids = ids

        return tdd

    def append(self, ts, row):

        if hasattr(self, 'timesteps') and (ts != self.timesteps[-1]+self.delta_t):
            raise RuntimeError("unable to append timestep... invalid ts")

        if len(row) != len(self.ids):
            raise RuntimeError("unable to append timestep... data is wrong length")


	if hasattr(self, 'data'):
	    self.timesteps.append(ts)
            self.data = numpy.vstack((self.data, row))
        else:
	    self.timesteps = [ts]
            self.data = numpy.array(row).reshape(1, len(row))

    @staticmethod
    def load(tdd_filename, id_filename = 'LinkIndex'):

        tdd = TDD()

        try:
            f = open(id_filename, "r")
            hdr = numpy.fromfile(f, hdr_type, 1)
            row_type = numpy.dtype([('junk', 'int32'), ('data', '(%d,)int32' % (hdr['ncols'][0]-1))])
            rowdata = numpy.fromfile(f, row_type, 1)
            tdd.ids = rowdata[0][1].tolist()
            f.close()
        except:
            raise RuntimeError("unable to load id_filename: %s" % id_filename)
        try:
            f = open(tdd_filename)
            hdr = numpy.fromfile(f, hdr_type, 1)
            tdd.delta_t = int(hdr['delta_t'])
            if hdr['nrows'] > 0:
				if hdr['type'] == IS_FLOAT:
					row_type = numpy.dtype([('ts', 'int32'), ('data', '(%d,)float32' % (hdr['ncols']-1))])
				else:
					row_type = numpy.dtype([('ts', 'int32'), ('data', '(%d,)int32' % (hdr['ncols']-1))])
					rowdata = numpy.fromfile(f, row_type, hdr['nrows'])
					tdd.timesteps = [int(a[0]) for a in rowdata]
					tdd.data = numpy.vstack([a[1] for a in rowdata])
            f.close()
        except:
            raise RuntimeError("unable to load tdd_filename: %s" % tdd_filename)

        tdd.id_map = {}
        for i in enumerate(tdd.ids):
            tdd.id_map[i[1]] = i[0]

        return tdd


    def save(self, filename):

	if hasattr(self, 'ids'):
	    ncols = len(self.ids)
	else:
	    ncols = 0

	if hasattr(self, 'timesteps'):
	    nrows = len(self.timesteps)
	else:
 	    nrows = 0

        try:
            hdr = [nrows, ncols+1, self.delta_t, nrows*ncols*4, self.type] + range(44)
            hdr_format = 'ii' + 'd' + 'i' + 'i' + 'i'*(44)

            f = open(filename, 'w')
            f.write(struct.pack(hdr_format, *hdr))

	    if nrows > 0:
		if type(self.data[0][0]) == numpy.float32:
		    row_format = 'i' + 'f'*ncols
		else:
		    row_format = 'i' + 'i'*ncols

		tsteps = numpy.array(self.timesteps).reshape(nrows, 1)
		for i in range(len(self.timesteps)):
		    row = [self.timesteps[i]] + list(self.data[i][:])
		    f.write(struct.pack(row_format, *row))

            f.close()
        except:
            raise RuntimeError("unable to save file as: %s" % filename)
