#pragma once
#include "../common/common.h"

struct LinkEdge{
    // 终点
    node_t to;
    // 边权重 
    weight_t w;
    // 同起点的上一条边的编号
    node_t next;

};
struct Graph_L{
    int n;
    int e;
    bool is_directed;
    bool is_deg;
    std::vector<int> head;
    std::vector<LinkEdge> edges;
    std::vector<int> degree;
    int max_deg = 0;
    Graph_L(int vetex_num = 0, bool directed = true, bool deg = false){
        this->n = vetex_num;
        this->e = 0;
        this->is_deg = deg;
        this->is_directed = directed;
        if(n > 0){
            head.resize(vetex_num + 1);
            if(deg){
                degree.resize(vetex_num + 1);
                for(int i = 0; i < vetex_num+1; i++){
                    head[i] = -1;
                    degree[i] = 0;
                }
            }
            else{
                for(int i = 0; i < vetex_num+1; i++){
                    head[i] = -1;
                }
            }   
        }
    }

    void add_unweighted_edge(const int &u, const int &v) {
        LinkEdge le;
        le.to = v;
        le.next = head[u];
        this->edges.emplace_back(le);  
        this->head[u] = this->e;
        this->e += 1;
        
        if(this->is_deg){
            this->degree[u]++;
            this->max_deg = std::max(this->max_deg, this->degree[u]);
        } 
    }

    void add_weighted_edge(const int &u, const int &v, const double &w) {
        LinkEdge le;
        le.to = v;
        le.w = w;
        le.next = head[u];
        this->edges.emplace_back(le);  
        this->head[u] = this->e;
        this->e += 1;
        if(this->is_deg){
            this->degree[u]++;
            this->max_deg = std::max(this->max_deg, this->degree[u]);
        } 
    }
};

struct compare_node {
	compare_node(){} 
    compare_node(int _x, int _d) {x = _x; d = _d;}
	int x, d;	
	bool operator < (const compare_node &rhs) const {
		return d > rhs.d;
	}
};