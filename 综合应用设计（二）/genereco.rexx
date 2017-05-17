/*************************REXX***********************/    
SPEND.0 = 3
SPEND.1 = 0
SPEND.2 = 0
SPEND.3 = 0
CALL LINEOUT RESULT.TXT, '交易流水号'||'   '||'交易人'||'   '||'交易数额'||'   '||'交易时间'||'   '||'交易类型'||'   '||'交易额度'
NUMERIC DIGITS 5                                          
USER.0 = 3
USER.1.NAME = 'XR000'
USER.2.NAME = 'XR001'
USER.3.NAME = 'XR002'
RECORD.0 = 60                                             
YEAR = 2016                                               
MONTH = 10                                                
DAY = 01                                                  
DO I = 1 TO RECORD.0                                      
   DAYTRANS = RANDOM(1,9)                                 
   RECORD.I.0 = DAYTRANS
   IF DAY == 20 THEN
      DO 
         CALL LINEOUT RESULT.TXT, SPEND.1 ||' '||SPEND.2||' '||SPEND.3
         SPEND.1 = 0
         SPEND.2 = 0
         SPEND.3 = 0
      END                                  
   DO J = 1 TO RECORD.I.0                        
      K = RANDOM(1,3)         
      RECORD.I.J.SERIAL = YEAR||MONTH||DAY||USER.K.NAME||J      
      RECORD.I.J.USER = USER.K.NAME                             
      RECORD.I.J.SPEND = RANDOM(100,200)  
      SPEND.K = SPEND.K + RECORD.I.J.SPEND
      RECORD.I.J.TIME = YEAR||MONTH||DAY                  
      RECORD.I.J.TYPE = RANDOM(0,1)                                
	   RECORD.I.J.MAXLIMIT = 5000            
   END                                      
   DAY = DAY + 1                            
   IF DAY < 10 THEN                         
	   DO                                    
	      DAY = 0||DAY                       
	   END                                   
   IF DAY == 31 THEN                        
	   DO                                    
	      MONTH = 11                         
	      DAY = 01                           
	   END                                   
   END       

DO I = 1 TO RECORD.0
   DO J = 1 TO RECORD.I.0 
       RESULT = RECORD.I.J.SERIAL||'  '||RECORD.I.J.USER||'   '||RECORD.I.J.SPEND||'  '||RECORD.I.J.TIME'  '||RECORD.I.J.TYPE||'  '||RECORD.I.J.MAXLIMIT
       CALL LINEOUT RESULT.TXT,RESULT
   END 
END    


/** ALLOCATE DATASET('ADCDMST.REXX.EXEC(FILE)') FILE(OUTADATA) OLD REUSE **/
/** EXECIO * DISKW OUTADATA (STEM RECORD.                                **/




 