import os
def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
def write_f(filename,save_dir,text,log_text):
    file_dir = str(save_dir)+"/"+str(filename).replace(" ","_").replace(":",".")+".txt"
    if not os.path.isfile(file_dir):
        with open(file_dir, "+w") as f:
            f.write(text.encode("gb18030").decode("utf-8",errors="ignore")+"\n")

        with open(str(save_dir)+"/log.txt","a") as log:
            log.write(log_text+"\n")
