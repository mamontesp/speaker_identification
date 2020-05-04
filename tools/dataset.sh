#!/bin/bash
main_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

help()
{
    echo ""
    echo "Usage $0 -d data_path -s step -r results_path"
    echo -e "\t-d Where dataset of wav files is stored"
    echo -e "\t-s Step you want to run"
    echo -e "\t-r Where new data is going to be stored"
    exit 1 #exit script after printing help
}

get_unique_speaker_id()
{
    echo "Parameter #1 is $1"
    filename_list=$(find $1 -name "*.wav")
    filename_basename=$(basename $filename_list)
    for name in ${filename_basename}
    do
        echo $(cut -d'_' -f2 <<< $name) >> speakers_id.txt
    done
    echo -e $(cat speakers_id.txt | sort | uniq ) > speakers_id.txt
}

store_speaker_files_by_id()
{
    echo "Main directory ${main_dir}"
    if [ -d "${main_dir}/../preprocessed_data/speakers" ]; then rm -Rf ${main_dir}/../preprocessed_data/speakers; fi
    mkdir ${main_dir}/../preprocessed_data/speakers
    results_dir="${main_dir}/../preprocessed_data/speakers"
    speakers_id=$(cat speakers_id.txt)
    count=0
    rm -rf dict_speakers.txt
    for speaker_id in ${speakers_id}
    do
        count=$((count+1))
        dict_speakers="dict_speakers.txt"
        echo -e "${count},${speaker_id}" >> ${dict_speakers}
        if [ -d "${results_dir}/${count}" ]; then rm -Rf ${results_dir}/${count}; fi
        mkdir ${results_dir}/S${count}
    done 
    search_files_by_speaker_id $1 ${dict_speakers} ${results_dir}
}

search_files_by_speaker_id()
{
    speakers=$(cat ${2} | sort | uniq )
    for speaker in ${speakers}
      do
        echo ${speaker} 
        IFS=","
        read -ra speaker_data  <<< "${speaker}"
        count=${speaker_data[0]}
        speaker_id=${speaker_data[1]}
        IFS=$'\n'
        coincident_filename_list=( $(find $1 -name "*$speaker_id*") )
        len=${#coincident_filename_list[@]}
        echo "Length $len"
        count_file_per_speaker=0
        for file in ${coincident_filename_list[@]}
            do
                echo "Copying"
                echo "Source ${file}"
                echo "Dest ${3}/S${count}/S${count}.${count_file_per_speaker}.wav"
                count_file_per_speaker=$((count_file_per_speaker+1))
                cp ${file} ${3}/S${count}/S${count}.${count_file_per_speaker}.wav
            done
    done
}

while getopts "d:s:r:" opt
do 
    case "$opt" in
    d ) data_path="$OPTARG" ;;
    s ) step="$OPTARG" ;;
    r ) if [-z "$OPTARG"]
        then 
            results_path="${main_dir}/../preprocessed_data"
            echo "Results path: ${results_path}"
        else
            results_path="$OPTARG"
        fi ;;
    ? ) help ;; #print help function in case parameter is not-existent
    esac
done


#Begin script in case all parameters are correct
echo "Path: $data_path"
case "$step" in
    1) get_unique_speaker_id "$data_path";;
    2) store_speaker_files_by_id "$data_path";;
    ? ) help ;; #print help function in case parameter is not-existent
esac

#Print help function in case parameters are empty
if [ -z "$step" ]
then
    echo "Some or all of the parameters are empty";
    help
fi
