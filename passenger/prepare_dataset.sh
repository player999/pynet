#!/bin/bash

classes_list="$(grep -Eo '^[^ ]+' classes.txt)"
tags_list="$(awk 'NF>1{print $NF}' classes.txt)"


declare -A class_map


for tag in $tags_list; 
do

    class="$(echo $classes_list | awk -v myvar="$tag" '{print $myvar}')";
    class_map["$tag"]=$class;

done


# class_map[0]="toyota"	 
# class_map[1]="vaz_(lada)" 
# class_map[2]="nissan" 
# class_map[3]="mercedes-benz" 
# class_map[4]="bmw" 
# class_map[5]="ford" 
# class_map[6]="hyundai" 
# class_map[7]="volkswagen" 
# class_map[8]="mitsubishi" 
# class_map[9]="chevrolet" 
# class_map[10]="kia" 
# class_map[11]="audi" 
# class_map[12]="honda" 
# class_map[13]="renault" 
# class_map[14]="opel"


rm output_train.txt;
rm output_test.txt;

touch output_train.txt;
touch output_test.txt;


for tag in $tags_list;
do

    file_path="$(find "${class_map[$tag]}" -maxdepth 3 -mindepth 3 -type f | head -100 | sort -R )"
    touch "temp_train.txt"
    touch "temp_test.txt"
    # echo "$file_path" >> temp.txt
    echo "$file_path" | head -80 >> temp_train.txt
    echo "$file_path" | tail -20 >> temp_test.txt

    sed -i "s/.jpg/.jpg ${tag}/g" ./temp_train.txt;
    sed -i "s/.jpg/.jpg ${tag}/g" ./temp_test.txt;
     
    cat temp_train.txt >> output_train.txt;
    cat temp_test.txt >> output_test.txt;
    
    rm ./temp_train.txt;
    rm ./temp_test.txt;

done

# Add '\' befor '/'
prefix="\/home\/player999\/Work\/VehicleClassification\/MMR1_3chan\/"
# prefix="\/passenger\/"

# Add prefix
sed -i -e "s/^/${prefix}/" ./output_test.txt;
sed -i -e "s/^/${prefix}/" ./output_train.txt;
