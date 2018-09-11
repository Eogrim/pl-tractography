
#!/bin/bash
# Bash script to install and powerup the FNNDSC mediawiki

SYNOPSIS="
NAME
        $0
ARGS
        [-p] test

DESCRIPTION
        $0 is a script that installs and runs the FNNDSC mediawiki
        containerized.
"

function synopsis_show
{
        echo "$SYNOPSIS"
        exit 1
}

declare -i Gi_verbose=0
declare -i Gb_useExpertOptions=1
declare -i Gb_useOverrideOut=0
declare -i Gb_forceStage=0
declare -i Gb_mailAll=0
declare -i Gb_mailStd=0
declare -i Gb_mailErr=0
declare -i Gb_mailLog=0
declare -i Gb_runCluster=0
declare -i Gb_useDICOMFile=0
declare -i Gb_useLowerThreshold1=0
declare -i Gb_useUpperThreshold1=0
declare -i Gb_useLowerThreshold2=0
declare -i Gb_useUpperThreshold2=0
declare -i Gb_useMask1=0
declare -i Gb_useMask2=0
declare -i Gb_useAngleThreshold=10
declare -i Gi_bValue=1000
declare -i Gb_bValueOverride=0
declare -i Gb_b0override=0
declare -i Gi_b0vols=1
declare -i Gb_Siemens=0
declare -i Gb_Philips=0
declare -i Gb_GE=0
declare -i Gb_forceGradientFile=0
declare -i Gb_skipEddyCurrentCorrection=0
declare -i Gb_GEGradientInlineFix=1
declare -i Gb_useDiffUnpack=1

while getopts "v: D: d: B: A: I: k E L: O: R: o: f \
                S: X Y Z t: c C: g: G U b: n: M: m: \
                m1: m2: \
                m1-lower-threshold: \
                m2-lower-threshold: \
                m1-upper-threshold: \
                m2-upper-threshold: \
                angle-threshold:    \
                migrate-analysis:" "options" ; do #!!!!!!!
        case "$options"
        in
            v)      Gi_verbose=$OPTARG              ;;
            D)      G_DICOMINPUTDIR=$OPTARG         ;;
            d)      Gb_useDICOMFile=1               
                    G_DICOMINPUTFILE=$OPTARG        ;;
            E)      Gb_useExpertOptions=1           ;;
            k)      Gb_skipEddyCurrentCorrection=1  ;;
            L)      G_LOGDIR=$OPTARG                ;;
            O)      Gb_useOverrideOut=1     
                    G_OUTDIR=$OPTARG                ;;
            R)      G_DIRSUFFIX=$OPTARG             ;;
            o)      G_OUTSUFFIX=$OPTARG             ;;
            g)      Gb_forceGradientFile=1  
                    G_GRADIENTFILE=$OPTARG          ;;
            B)      Gb_b0override=1
                    Gi_b0vols=$OPTARG               ;;
            I)      G_IMAGEMODEL=$OPTARG            ;;
            A)      G_RECONALG=$OPTARG              ;;
            m1)     Gb_useMask1=1
                    G_MASKIMAGE1=$OPTARG            ;;
            m1-lower-threshold)
                    Gb_useLowerThreshold1=1
                    G_LOWERTHRESHOLD1=$OPTARG       ;;        
            m1-upper-threshold)
                    Gb_useUpperThreshold1=1                            
                    G_UPPERTHRESHOLD1=$OPTARG       ;;                                       
            m2)     Gb_useMask2=1
                    G_MASKIMAGE2=$OPTARG            ;;           
            m2-lower-threshold)
                    Gb_useLowerThreshold2=1                            
                    G_LOWERTHRESHOLD2=$OPTARG       ;;                    
            m2-upper-threshold)
                    Gb_useUpperThreshold2=1                            
                    G_UPPERTHRESHOLD2=$OPTARG       ;;
            angle-threshold) 
                    Gb_useAngleThreshold=1
                    G_ANGLETHRESHOLD=$OPTARG        ;;                                                               
            G)      Gb_GEGradientInlineFix=0        ;;
            S)      G_DICOMSERIESLIST=$OPTARG       ;;
            f)      Gb_forceStage=1                 ;;
            t)      G_STAGES=$OPTARG                ;;
            c)      Gb_runCluster=1                 ;;
            C)      G_CLUSTERDIR=$OPTARG            ;;
            U)      Gb_useDiffUnpack=0              ;;
            b)      Gb_bValueOverride=1
                    Gi_bValue=$OPTARG               ;;
            X)      G_iX="-X"                       ;;
            Y)      G_iY="-Y"                       ;;
            Z)      G_iZ="-Z"                       ;;
            M)      Gb_mailStd=1
                    Gb_mailErr=1
                    G_MAILTO=$OPTARG                ;;
            m)      Gb_mailStd=1
                    Gb_mailErr=0
                    G_MAILTO=$OPTARG                ;;
            n)      G_CLUSTERUSER=$OPTARG           ;;
            migrate-analysis)
                    G_MIGRATEANALYSISDIR=$OPTARG    ;;

            \?)     synopsis_show 
                    exit 0;;
        esac
done

echo "G_ANGLETHRESHOLD = "$G_ANGLETHRESHOLD
echo "Gi_verbose = "$Gi_verbose
echo "G_GRADIENTFILE = "$G_GRADIENTFILE
echo "G_LOWERTHRESHOLD1 = "$G_LOWERTHRESHOLD1
echo "G_STAGES = "$G_STAGES
echo "G_MAILTO = "$G_MAILTO
echo "Gi_bValue = "$Gi_bValue
