#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define REALLOC_FAILURE 1
#define LIST_IDX_OUT_OF_RANGE 2

//Util functions
void errorprint(char* error_msg, int errorcode){
    printf("%s\n\n", error_msg);
    exit(errorcode);
}

char* bool_to_str(bool var){
    return var ? "True" : "False";
}

//################################List###############################

typedef struct{
    void* element;
    char* type;
} list_element_t;

typedef struct {
    int length;
    list_element_t* list_content;
} list_t;

list_t list_create() {
    list_t new_list;
    new_list.length = 0;
    new_list.list_content = NULL;
    return new_list;
}

list_t list_append(list_t list, char* type, void* element) {
    list.length++;

    list.list_content = (list_element_t*)realloc(list.list_content, list.length * sizeof(list_element_t));

    if (list.list_content == NULL){
        errorprint("Fatal Error: Failed reallocation during list_append() function for instance of type list_t!", REALLOC_FAILURE);
    }

    list_element_t new_element;
    new_element.element = element;
    new_element.type = strdup(type);

    list.list_content[list.length-1] = new_element;

    return list;
}

list_t list_insert(list_t list, int index, char* type, void* element){
    list.length = list.length+1;

    list.list_content = (list_element_t*)realloc(list.list_content, list.length * sizeof(list_element_t));

    if (list.list_content == NULL){
        errorprint("Fatal Error: Failed reallocation during list_insert() function for instance of type list_t!", REALLOC_FAILURE);
    }

    for (int i=list.length-2;i>=index;i--){
        list.list_content[i+1] = list.list_content[i];
    }

    list_element_t new_element;
    new_element.element = element;
    new_element.type = strdup(type);

    list.list_content[index] = new_element;
    
    return list;
}

list_element_t list_get(list_t list, int index){
    if (index >= list.length){
        errorprint("List index out of range!", LIST_IDX_OUT_OF_RANGE);
    }
    return list.list_content[index];
}

char* list_print(list_t list) {
    char* output = (char*)malloc(1024 * sizeof(char)); // Large buffer for simplicity
    output[0] = '\0';

    strcat(output, "[");
    for (int i = 0; i < list.length; i++) {
        list_element_t cur_list_element = list.list_content[i];
        void* cur_element = cur_list_element.element;
        char* type = cur_list_element.type;

        if (strcmp(type, "str") == 0) {
            char* element = (char*)cur_element;
            strcat(output, element);
        } else if (strcmp(type, "int") == 0) {
            int element = *(int*)cur_element;
            char buffer[50];
            sprintf(buffer, "%d", element);
            strcat(output, buffer);
        } else if (strcmp(type, "float") == 0) {
            float element = *(float*)cur_element;
            char buffer[50];
            sprintf(buffer, "%f", element);
            strcat(output, buffer);
        } else if (strcmp(type, "bool") == 0) {
            bool element = *(bool*)cur_element;
            strcat(output, bool_to_str(element));
        } else if (strcmp(type, "list") == 0) {
            list_t list_element = *(list_t*)cur_element;
            char* element = list_print(list_element);
            strcat(output, element);
            free(element);
            free(cur_element);
        }
        
        if (i != list.length - 1) {
            strcat(output, ", ");
        }
    }
    strcat(output, "]");
    return output;
}

//##############################Test Programm##########################

int main() {
    list_t test_list = list_create();

    char* test_element_1 = "This is an element";

    char* test_element_2 = "This is a different element";

    for (int i=0;i<5;i++){
        test_list = list_append(test_list, "str", (void*)test_element_1);
    }

    test_list = list_insert(test_list, 0, "str", (void*)test_element_2);
    
    char* output = list_print(test_list);
    printf("%s\n", output);

    free(output);

    printf("%s\n", "");
    return 0;
}
