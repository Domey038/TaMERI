#Library initializations
suppressMessages(library("data.table"))
suppressMessages(library(magrittr))
suppressMessages(library(tidyr))
suppressMessages(library(ggplot2))
suppressMessages(library(stringr))

#----------------------------------------#
#             Preprocessing              #
#----------------------------------------#
#Commandline input
args = commandArgs(trailingOnly=TRUE)
if (length(args) != 2) {
  print("")
  stop("Required input:\n<TaMERI/data/cv_results.X> <ML algorithm>")
}

#DEBUG - START
#args <- c("/home/domey/Studium-Shit/Master/SS_2018/Masterarbeit/working_dir/TaMERI/data/cv_results.RF")
#DEBUG - END

#Parameter
data_set <- "homo_sapiens"
ML_algorithm <- args[2]

#Initialize dt_complete (which contains the validation results of all cross-validation folds)
cv_dt_PATH <- file.path(args[1], "data.tsv")
cv_dt <- fread(cv_dt_PATH, sep="\t", header=TRUE)

#Preprocessing
cv_dt$fold = as.factor(cv_dt$fold)

#Plot simple obs vs pred Scatterplot
plotVS <- ggplot(cv_dt, aes(real, pred, col=fold)) + 
  geom_point() + 
  geom_abline() + 
  facet_wrap(~ fold, scale="free") + 
  theme(legend.position="none") +
  xlab("TM/EM ER ratio - Observed") + 
  ylab("TM/EM ER ratio - Predicted") + 
  ggtitle("Calibration scatterplot", 
          paste(paste("ML algorithm:", ML_algorithm, sep=" "),
                paste("Data set:", data_set, sep=" "), sep="\n"
          ))
outputPath = file.path(paste("predictive_power", "scatterplot", "png", sep="."))
png(outputPath, 1600,1200, res=180)
suppressWarnings(print(plotVS))
out <- dev.off()

#Preprocessing for trend accuracy
#cv_cons_dt <- cv_dt[, .(real_cons=real>0, pred_cons=pred>0, fold)]
#table(cv_cons_dt[,c("real_cons","pred_cons")])

#Preprocessing for accuracy vs cutoff
ae <- cv_dt[, .(absolute_error=abs(real-pred), fold=fold)]
calc_accuracy <- function(cutoff, df){
  acc <- df[, .(accuracy=sum(absolute_error<=cutoff)/.N, abs_error_cutoff=cutoff), by=fold]
  return(acc)
}
diff_cutoffs <- seq(0, 0.03, 0.03/100)
acc_df <- lapply(diff_cutoffs, calc_accuracy, ae) %>%
  rbindlist(.)

#Plot accurcy vs absolute error cutoff
plotAcc <- ggplot(acc_df, aes(abs_error_cutoff, accuracy, col=fold)) + 
  geom_vline(xintercept=0.0025, linetype="dashed", col="black") + 
  geom_vline(xintercept=0.0050, linetype="dashed", col="black") +
  geom_line(size=1) +   
  scale_x_continuous(limits=c(0,0.03),
                     breaks = round(seq(0, 0.03, by = 0.0025),4)) + 
  scale_y_continuous(limits=c(0,1.0),
                     breaks = round(seq(min(acc_df$accuracy), 1, by = 0.1), 1)) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) + 
  xlab("Absolute error cutoff") + 
  ylab("Accuracy") + 
  ggtitle("Accuracy vs accepted abs error range", 
          paste(paste("ML algorithm:", ML_algorithm, sep=" "),
                paste("Data set:", data_set, sep=" "), sep="\n"
                ))
outputPath = file.path(paste("predictive_power", "accuracy", "png", sep="."))
png(outputPath, 1600,1200, res=220)
suppressWarnings(print(plotAcc))
out <- dev.off()

#Error distribution - Histogram
plotErr <- ggplot(ae, aes(absolute_error)) + 
  geom_histogram(bins=100, col="black", fill=heat.colors(100)) + 
  xlim(0, 0.025) + 
  xlab("Absolute error") + 
  ylab("Frequency") + 
  ggtitle("Absolute error distribution", 
          paste(paste("ML algorithm:", ML_algorithm, sep=" "),
                paste("Data set:", data_set, sep=" "), sep="\n"
          ))
outputPath = file.path(paste("error_distribution", "png", sep="."))
png(outputPath, 1600,1200, res=220)
suppressWarnings(print(plotErr))
out <- dev.off()

#Error vs real - Scatterplot
err_dt <- cbind(cv_dt, error=abs(cv_dt$real-cv_dt$pred))
plotErrReal <- ggplot(err_dt, aes(real, error, col=fold)) + 
  geom_point(size=0.75) + 
  geom_hline(yintercept=0, linetype="dashed", size=0.25, col="black") + 
  xlim(-0.025, 0.025) + 
  ylim(0, 0.025) + 
  xlab("Observed TM/EM ER ratio") + 
  ylab("Absolute error") + 
  ggtitle("Absolute error association to observations", 
          paste(paste("ML algorithm:", ML_algorithm, sep=" "),
                paste("Data set:", data_set, sep=" "), sep="\n"
          ))
outputPath = file.path(paste("error_vs_observed", "png", sep="."))
png(outputPath, 1600,1200, res=220)
suppressWarnings(print(plotErrReal))
out <- dev.off()


#Error vs real - Scatterplot
err_dt <- cbind(cv_dt, error=abs(cv_dt$real-cv_dt$pred))
plotErrReal <- ggplot(err_dt, aes(real, error, col=fold)) + 
  geom_point(size=0.75) + 
  geom_hline(yintercept=0, linetype="dashed", size=0.25, col="black") + 
  xlim(-0.025, 0.025) + 
  ylim(0, 0.025) + 
  xlab("Observed TM/EM ER ratio") + 
  ylab("Absolute error") + 
  ggtitle("Absolute error association to observations", 
          paste(paste("ML algorithm:", ML_algorithm, sep=" "),
                paste("Data set:", data_set, sep=" "), sep="\n"
          ))
outputPath = file.path(paste("error_vs_observed", "png", sep="."))
png(outputPath, 1600,1200, res=220)
suppressWarnings(print(plotErrReal))
out <- dev.off()

#Residual plot
cv_dt[, residual:= real-pred]
plotResiduals <- ggplot(cv_dt, aes(pred, residual, col="red")) + 
  geom_point(size=0.75) + 
  geom_smooth(method="lm", col="cyan", size=1) + 
  geom_hline(yintercept=0, linetype="dashed", size=0.25, col="black") + 
  xlab("Predicted TM/EM ER ratios") + 
  ylab("Residuals") + 
  theme(legend.position="none") + 
  ggtitle("Residuals vs Fitted TM/EM ER ratios", 
          paste(paste("ML algorithm:", ML_algorithm, sep=" "),
                paste("Data set:", data_set, sep=" "), sep="\n"
          ))
outputPath = file.path(paste("residual_vs_fitted", "png", sep="."))
png(outputPath, 1600,1200, res=220)
suppressWarnings(print(plotResiduals))
out <- dev.off()


#Real AAIMON slope distribution
real_quantiles <- quantile(cv_dt$real, probs=seq(0,1,0.05))
plot_real_distribution <- ggplot(cv_dt, aes(real)) + 
  geom_histogram(bins=100, col="black", fill=heat.colors(100)) + 
  geom_vline(xintercept=0, linetype="dashed", size=0.75, col="black") + 
  geom_vline(xintercept=real_quantiles[2], linetype="dashed", size=0.75, col="blue") + 
  geom_vline(xintercept=real_quantiles[20], linetype="dashed", size=0.75, col="blue") + 
  xlab("Korbinian TM/EM ER ratios") + 
  ylab("Frequency") + 
  scale_x_continuous(breaks = round(seq(min(cv_dt$real), max(cv_dt$real), by = 0.0025), 4)) +
  theme(axis.text.x = element_text(angle = 60, hjust = 1)) + 
  ggtitle("Korbinian TM/EM ER ratio distribution")
outputPath = file.path(paste("residual_vs_fitted", "png", sep="."))
png(outputPath, 1600,1200, res=220)
suppressWarnings(print(plotResiduals))
out <- dev.off()

#Calculate value range
value_range <- abs(real_quantiles[20]) + abs(real_quantiles[2])
print(value_range * 10/100)
