import random

def insertError(codeword,count):
    if len(codeword)<count:
        return codeword
    else:
        flip_positions=[0]*len(codeword)
        while count>0:
            randomposition=random.randint(0,len(codeword)-1)
            if(not flip_positions[randomposition]):
                flip_positions[randomposition]=1
                count-=1
        modified_data=""
        for i in range(0,len(codeword)):
            try:
                if(flip_positions[i]):
                    modified_data+=str(int(codeword[i],2)^1)
                else:
                    modified_data+=codeword[i]
            except:
                print(codeword[i],":","Expected bit only! From Error injection")
                return None
        return modified_data

if __name__=='__main__':
    codeword="11011000100000001000001111110001010110000100001011011000100000001000001111110001010110000100001011000000000100010110"
    count=3
    print(insertError(codeword,count)) 