##
## Barto multisegment plot
##
setwd("~/Google_Drive/@ASU2020/Paramecium/paramecium-jf/pairwise_F1X4")

## Load library & data
library(genoPlotR)
data(barto)

## Saving data
## Uncomment the two commented lines if you wish to save the figures
## on your desktop
imgPath <- "../img"
pdfPath <- "../pdfs"
#imgPath <- "~/Desktop"
#pdfPath <- "~/Desktop"

## Adding a tree
tree <- newick2phylog("(BB:2.5,(BG:1.8,(BH:1,BQ:0.8):1.9):3);")
## Showing several subsegments per genome
xlims2 <- list(c(1445000, 1415000, 1380000, 1412000),
               c(  10000,   45000,   50000,   83000, 90000, 120000),
               c(  15000,   36000,   90000,  120000, 74000,  98000),
               c(   5000,    82000))
## Adding annotations for all genomes
annots <- lapply(barto$dna_segs, auto_annotate, rot=30)
## Keeping only one every 4 annots
annots <- lapply(annots, function(x) x[(1:nrow(x))%%3 == 0,])
## Adding fake data in 1kb windows
seg_plots <- lapply(barto$dna_segs, function(ds){
  x <- seq(1, range(ds)[2], by=1000)
  y <- jitter(seq(100, 300, length=length(x)), amount=50)
  seg_plot(func=linesGrob, args=list(x=x, y=y, gp=gpar(col=grey(0.3), lty=2)))
})

## Plots
png(file.path(imgPath, "barto_seg_plots.png"), h=300, w=500)
plot_gene_map(barto$dna_segs, barto$comparisons, tree=tree,
              annotations=annots,
              seg_plots=seg_plots,
              seg_plot_height=1.5,
              seg_plot_height_unit="null",
              seg_plot_yaxis=2,
              seg_plot_yaxis_cex=0.8,
              xlims=xlims2,
              dna_seg_scale=TRUE,
              main="Random data on multi-segment plot, 4 Bartonella genomes")
dev.off()
cairo_pdf(file.path(pdfPath, "barto_seg_plots.pdf"), h=4, w=7)
plot_gene_map(barto$dna_segs, barto$comparisons, tree=tree,
              annotations=annots,
              seg_plots=seg_plots,
              seg_plot_height=1.5,
              seg_plot_height_unit="null",
              seg_plot_yaxis=2,
              seg_plot_yaxis_cex=0.8,
              xlims=xlims2,
              dna_seg_scale=TRUE,
              main="Random data on multi-segment plot, 4 Bartonella genomes")
dev.off()