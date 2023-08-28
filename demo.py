import simple_record
import time

recorder= simple_record.MouseRecorder(10)
recorder.start()
time.sleep(5)
recorder.stop()
print(recorder.position_list)