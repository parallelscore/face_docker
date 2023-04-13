
class SkipFrames:

  def __init__(self,n_steps=100, frame_count=None):
    self.n_steps = n_steps
    self.frame_count = frame_count


  def get_n_step_frames(self,local_frames_length):
    assert self.n_steps < local_frames_length-1,f"The number of steps you picked is greater than the number of frames available: There are {local_frames_length} number frames."
    return [i for i in range(0,local_frames_length-1,self.n_steps)]

  def frames_btw_n_steps(self, steps):
    all_nodes = []

    if self.frame_count  is None:
        self.frame_count = int(self.n_steps/6)
    else:
      self.frame_count = int(self.n_steps/self.frame_count)
   
    for i in range(len(steps)):
        if i == len(steps)-1:
            continue
        else:
            all_nodes.extend([i for i in range(steps[i], steps[i+1],self.frame_count)])
    return all_nodes

  def extract_n_frames(self, local_frame_length):

    key_steps = self.get_n_step_frames(local_frame_length)
    final_frames_indexes = self.frames_btw_n_steps(key_steps)
    print(f'The number of frames have been reduced from {local_frame_length-1} to {len(final_frames_indexes)}.')
    return final_frames_indexes
