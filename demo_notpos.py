import os,CRFPP,jieba
#jieba.load_userdict("lcljieba.txt")
def load_model(path):
    if os.path.exists(path):
        return CRFPP.Tagger('-m{0} -v 3 -n 2'.format(path))
    return None

def locationNER(text):
    tagger=load_model('model')
    for c in jieba.lcut(text):
        if len(c)==1:
            tagger.add(c+'\t'+'S')	
        else:
            for i in range(len(c)):
                if i==0:
                    tagger.add(c[i]+'\t'+'B')
                elif i<len(c)-1:
                    tagger.add(c[i]+'\t'+'M')
                else:
                    tagger.add(c[i]+'\t'+'E')
    result=[]
    r=[]
    tagger.parse()
    word=""
    count=0
    for i in range(0,tagger.size()):
        for j in range(0,tagger.xsize()):
            count+=1
            ch=tagger.x(i,j)
            tag=tagger.y2(i)
            print("========",tag)
            print(count)
            if count%2==1:
                if "B-" in tag:
                    if word=="":
                        word=ch
                        r.append(tag[2:])
                    else:
                        result.append(word)
                        word=""
                elif "M-" in tag:
                    word+=ch
                elif "E-" in tag:
                    word+=ch
                elif "O" in tag:
                    if word!="":
                        result.append(word)
                        word=""
                if "S-" in tag:
                    if word=="":
                        word=ch
                        result.append(word)
                        r.append(tag[2:])
                    else:
                        result.append(word)
    if word!="":
        result.append(word)
    print(result,r)
    return result,r

def test_predict(text):
    result,r=locationNER(text)
    s=""
    for i in range(len(r)): 
        s+=r[i]+":"+result[i]+'\n'
    return s
if __name__=="__main__":
    text='s'
    print("关闭请按enter键"+'\n')
    while text!='':
        text=input("请输入一个句子"+'\n')
        print(text,test_predict(text),sep="==>")
        
    
