#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include <mmsystem.h>

#pragma comment(lib, "winmm.lib")

typedef struct Node {
    char songName[100];
    char songPath[200];
    struct Node* prev;
    struct Node* next;
} Node;

Node* head = NULL;
Node* current = NULL;

// Create a new node
Node* createNode(char* name, char* path) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    strcpy(newNode->songName, name);
    strcpy(newNode->songPath, path);
    newNode->prev = newNode->next = NULL;
    return newNode;
}

// Add song to end
void addSong(char* name, char* path) {
    Node* newNode = createNode(name, path);
    if (!head) {
        head = newNode;
        current = head;
        return;
    }
    Node* temp = head;
    while (temp->next) temp = temp->next;
    temp->next = newNode;
    newNode->prev = temp;
}

// Display playlist
void displayPlaylist() {
    Node* temp = head;
    printf("\nPlaylist:\n");
    while (temp) {
        if (temp == current)
            printf(">> %s\n", temp->songName);
        else
            printf("   %s\n", temp->songName);
        temp = temp->next;
    }
}

// Play current song
void playSong() {
    if (!current) {
        printf("No songs to play!\n");
        return;
    }
    char command[300];
    sprintf(command, "close song");
    mciSendString(command, NULL, 0, NULL); // close previous
    sprintf(command, "open \"%s\" type mpegvideo alias song", current->songPath);
    mciSendString(command, NULL, 0, NULL);
    mciSendString("play song", NULL, 0, NULL);
    mciSendString("play song repeat", NULL, 0, NULL);
    printf("Playing: %s\n", current->songName);
}

// Next song
void nextSong() {
    if (current && current->next) {
        current = current->next;
        playSong();
    } else {
        printf("No next song.\n");
    }
}

// Previous song
void prevSong() {
    if (current && current->prev) {
        current = current->prev;
        playSong();
    } else {
        printf("No previous song.\n");
    }
}

// Save playlist to file
void savePlaylist() {
    FILE* fp = fopen("playlist.txt", "w");
    if (!fp) return;
    Node* temp = head;
    while (temp) {
        fprintf(fp, "%s|%s\n", temp->songName, temp->songPath);
        temp = temp->next;
    }
    fclose(fp);
}

// Load playlist from file
void loadPlaylist() {
    FILE* fp = fopen("playlist.txt", "r");
    if (!fp) return;
    char line[300];
    while (fgets(line, sizeof(line), fp)) {
        line[strcspn(line, "\n")] = 0; // remove newline
        char* token = strtok(line, "|");
        if (!token) continue;
        char name[100], path[200];
        strcpy(name, token);
        token = strtok(NULL, "|");
        if (!token) continue;
        strcpy(path, token);
        addSong(name, path);
    }
    fclose(fp);
}

// Command-line controlled playback for web integration
void handleCommandLine(int argc, char* argv[]) {
    if (argc > 1) {
        if (strcmp(argv[1], "play") == 0 && argc > 2) {
            char* path = argv[2];
            // Set current to matching song
            Node* temp = head;
            while (temp) {
                if (strcmp(temp->songPath, path) == 0) {
                    current = temp;
                    break;
                }
                temp = temp->next;
            }
            playSong();
        } else if (strcmp(argv[1], "next") == 0) {
            nextSong();
        } else if (strcmp(argv[1], "prev") == 0) {
            prevSong();
        }
        exit(0);
    }
}
int main(int argc, char* argv[]) {
    loadPlaylist();

    if (argc > 1) { // Command-line call
        if (strcmp(argv[1], "play") == 0 && argc > 2) {
            char* path = argv[2];
            // Set current to matching song or create a temp node
            Node* temp = head;
            while (temp) {
                if (strcmp(temp->songPath, path) == 0) {
                    current = temp;
                    break;
                }
                temp = temp->next;
            }
            if (!current) { // song not in playlist yet
                addSong("TempSong", path);
                current = head;
            }
            playSong();
            Sleep(5000); // wait 5 seconds so song can start
        }
        return 0;
    }

}
