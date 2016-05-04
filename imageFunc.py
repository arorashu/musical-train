#   iterate through each pixel in an image and
#   determine the average rgb color

# you will need to install the PIL module

from PIL import Image

class PixelCounter(object):
  ''' loop through each pixel and average rgb '''
  def __init__(self, imageName):
      self.pic = Image.open(imageName)
      # load image data
      self.imgData = self.pic.load()
  def averagePixels(self):
      r, g, b = 0, 0, 0
      count = 0
      for x in xrange(self.pic.size[0]):
          for y in xrange(self.pic.size[1]):
              tempr,tempg,tempb = self.imgData[x,y]
              r += tempr
              g += tempg
              b += tempb
              count += 1
      # calculate averages
      return (r/count), (g/count), (b/count), count

if __name__ == '__main__':
  # assumes you have a test.jpg in the working directory! 
  pc = PixelCounter('test.jpg')
  print "(red, green, blue, total_pixel_count)"
  print pc.averagePixels()[0:3]