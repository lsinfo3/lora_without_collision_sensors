require(pracma)
library(readr)
#payloads <-c(8,10,12,16,24)
#slotlengths <- c(991,1318,1482,1810)
#slotlengthsalias<-c(8,16,24,32)
SFs<-c(7,8,9,10,11,12)
payloads<-c(8)
guardtimes<-c(1,2,5,7,9,10,12,15,17,20,25,30)
percentthresholds<-c(1,2,5,10,15,20,25)

Percentages<-matrix(nrow=length(percentthresholds),ncol = length(guardtimes))
i <-1
for(sf in SFs){
for (pl in payloads) {
  for (gt in guardtimes){
    current <- read_csv(paste("~/Sensors10000 SF",sf," PL",pl," SL8", " GT",gt,".csv",sep=""))
    X<-current$X
    collisions<-current$collisions
    png(paste("Sensors10000 SF",sf," PL",pl," SL8", " GT",gt,".png",sep=""), width = 500, height = 500)
    plot(X,collisions, xlab = "Number of Sensors", ylab = paste("Collision probability % SF",sf," GT %",gt),log="x")
    grid(nx = NULL,
         ny = NULL,
         col = "lightgray",
         lty = "dotted")
    dev.off()
    for (x in 1:length(percentthresholds)){
      Percentages[x,i]<-min(which(collisions > percentthresholds[x]/100))*10
      Percentages[x,i]<-ifelse(is.infinite(Percentages[x,i]),10000,Percentages[x,i])
    }
    i<-i+1
  }
  i<-1
  for (x in 1:length(percentthresholds)){
  png(paste("SF_",sf,"_PL_",pl,"_Percentage_",percentthresholds[x],".png",sep=""), width = 500, height = 500)
  plot(guardtimes,Percentages[x,],xlab = "Guard Time %", ylab = paste("Number of devices before ",percentthresholds[x],"% collision probability payload", pl))
  grid(nx = NULL,
       ny = NULL,
       col = "lightgray",
       lty = "dotted")
  dev.off()
}}}