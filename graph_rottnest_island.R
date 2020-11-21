
#############################################
#                                           #
#                                           #
#                                           #
#                onshore                    #
#                                           #
#                                           #
#                                           #
#############################################
mhws_onshore = read.csv("Rottnest_Island_onshore_biased_analys.csv",header = TRUE,colClasses=c("numeric","Date","Date","numeric","Date","numeric","numeric","numeric"))
mhws_freq_3year = read.csv("average_3_year_Rottnest_Island_onshore_biased_analys.csv",header = TRUE)
mhws_freq_peryear = read.csv("average_per_year_Rottnest_Island_onshore_biased_analys.csv",header = TRUE)

#plot of duration against date
scatter.smooth(x=mhws_onshore$time_start, y=mhws_onshore$duration,xlab="Starting time of mhws",ylab="Duration of mhws",main="Duration ~ Date : Rottnest Island Onshore",ylim=c(5,25))
Duration_vs_date <- lm(mhws_onshore$duration ~ mhws_onshore$time_start,subset=(mhws_onshore$duration < 25))
abline(Duration_vs_date,col="red")



#plot of duration against intensity
scatter.smooth(x=mhws_onshore$max_intensity, y=mhws_onshore$duration,xlab="Max intensity of mhws",ylab="Duration of mhws",main="Duration ~ Max intensity : Rottnest Island Onshore",ylim=c(5,25))
Duration_vs_mean_intensity <- lm(mhws_onshore$duration ~ mhws_onshore$max_intensity,subset=(mhws_onshore$duration < 25))
abline(Duration_vs_mean_intensity,col="red")


#plot of max intensity against date
scatter.smooth(x=mhws_onshore$time_start, y=mhws_onshore$max_intensity,xlab="Staring time of mhws",ylab="Max intensity of mhws",main="Max intensity ~ Date : Rottnest Island Onshore")
Max_intensity_vs_date <- lm(mhws_onshore$max_intensity ~ mhws_onshore$time_start)
abline(Max_intensity_vs_date,col="red")



#plot of mean intensity against date
plot(x=mhws_onshore$time_start, y=mhws_onshore$mean_intensity,xlab="Staring time of mhws",ylab="Mean intensity of mhws",main="Max intensity ~ Date : Rottnest Island Onshore",type="b")
Mean_intensity_vs_date <- lm(mhws_onshore$mean_intensity ~ mhws_onshore$time_start)
abline(Mean_intensity_vs_date,col="red")


barplot(as.table(setNames(mhws_freq_peryear$frequency,mhws_freq_peryear$start_year)),xlab="Year",ylab="number of mhws",main="Rottnest Island Onshore",border="red",col="blue",density=60)

barplot(as.table(setNames(mhws_freq_3year$frequency,mhws_freq_3year$centre_year)),xlab="Year",ylab="number of mhws",main="Rottnest Island Onshore",border="red",col="blue",density=60)



#############################################
#                                           #
#                                           #
#                                           #
#                offshore                   #
#                                           #
#                                           #
#                                           #
#############################################

mhws_offshore = read.csv("Rottnest_Island_offshore_biased_analys.csv",header = TRUE,colClasses=c("numeric","Date","Date","numeric","Date","numeric","numeric","numeric"))
mhws_freq_3year_off = read.csv("average_3_year_Rottnest_Island_offshore_biased_analys.csv",header = TRUE)
mhws_freq_peryear_off = read.csv("average_per_year_Rottnest_Island_offshore_biased_analys.csv",header = TRUE)

#plot of duration against date
scatter.smooth(x=mhws_offshore$time_start, y=mhws_offshore$duration,xlab="Starting time of mhws",ylab="Duration of mhws",main="Duration ~ Date : Rottnest Island Offshore",ylim=c(5,25))
Duration_vs_date <- lm(mhws_offshore$duration ~ mhws_offshore$time_start,subset=(mhws_offshore$duration < 25))
abline(Duration_vs_date,col="red")



#plot of duration against intensity
scatter.smooth(x=mhws_offshore$max_intensity, y=mhws_offshore$duration,xlab="Max intensity of mhws",ylab="Duration of mhws",main="Duration ~ Max intensity : Rottnest Island Offshore",ylim=c(5,25))
Duration_vs_mean_intensity_off <- lm(mhws_offshore$duration ~ mhws_offshore$max_intensity,subset=(mhws_offshore$duration < 25))
abline(Duration_vs_mean_intensity_off,col="red")


#plot of max intensity against date
scatter.smooth(x=mhws_offshore$time_start, y=mhws_offshore$max_intensity,xlab="Staring time of mhws",ylab="Max intensity of mhws",main="Max intensity ~ Date : Rottnest Island Offshore")
Max_intensity_vs_date_off <- lm(mhws_offshore$max_intensity ~ mhws_offshore$time_start)
abline(Max_intensity_vs_date_off,col="red")



#plot of mean intensity against date
plot(x=mhws_onshore$time_start, y=mhws_onshore$mean_intensity,xlab="Staring time of mhws",ylab="Mean intensity of mhws",main="Max intensity ~ Date : Rottnest Island Offshore",type="b")
Mean_intensity_vs_date_off <- lm(mhws_offshore$mean_intensity ~ mhws_offshore$time_start)
abline(Mean_intensity_vs_date_off,col="red")


barplot(as.table(setNames(mhws_freq_peryear_off$frequency,mhws_freq_peryear_off$start_year)),xlab="Year",ylab="number of mhws",main="Rottnest Island Offshore",border="red",col="blue",density=60)

barplot(as.table(setNames(mhws_freq_3year_off$frequency,mhws_freq_3year_off$centre_year)),xlab="Year",ylab="number of mhws",main="Rottnest Island Offshore",border="red",col="blue",density=60)
