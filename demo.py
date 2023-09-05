import simple_record
import time

recorder= simple_record.InputRecorder('q')
recorder.start()
time.sleep(5)
recorder.stop()
save= simple_record.RecorderSave()
recorder.export(save)
save.write("233")
replay=simple_record.Replayer(save)
replay.replay()