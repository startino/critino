export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  public: {
    Tables: {
      agents: {
        Row: {
          created_at: string
          description: string
          environment_name: string
          name: string
          team_name: string
          workflow_name: string
        }
        Insert: {
          created_at?: string
          description?: string
          environment_name: string
          name: string
          team_name: string
          workflow_name: string
        }
        Update: {
          created_at?: string
          description?: string
          environment_name?: string
          name?: string
          team_name?: string
          workflow_name?: string
        }
        Relationships: [
          {
            foreignKeyName: "agents_workflows_project_team_fkey"
            columns: ["team_name", "environment_name", "workflow_name"]
            isOneToOne: false
            referencedRelation: "workflows"
            referencedColumns: ["team_name", "environment_name", "name"]
          },
        ]
      }
      critiques: {
        Row: {
          agent_name: string
          context: string
          created_at: string
          environment_name: string
          id: string
          instructions: string
          optimal: string
          query: string
          response: string
          tags: string[]
          team_name: string
          workflow_name: string
        }
        Insert: {
          agent_name: string
          context?: string
          created_at?: string
          environment_name: string
          id: string
          instructions?: string
          optimal?: string
          query?: string
          response?: string
          tags?: string[]
          team_name: string
          workflow_name: string
        }
        Update: {
          agent_name?: string
          context?: string
          created_at?: string
          environment_name?: string
          id?: string
          instructions?: string
          optimal?: string
          query?: string
          response?: string
          tags?: string[]
          team_name?: string
          workflow_name?: string
        }
        Relationships: [
          {
            foreignKeyName: "critiques_agents_workflows_environment_team_fkey"
            columns: [
              "team_name",
              "environment_name",
              "workflow_name",
              "agent_name",
            ]
            isOneToOne: false
            referencedRelation: "agents"
            referencedColumns: [
              "team_name",
              "environment_name",
              "workflow_name",
              "name",
            ]
          },
        ]
      }
      environments: {
        Row: {
          created_at: string
          description: string
          key: string | null
          name: string
          parent_name: string | null
          team_name: string
        }
        Insert: {
          created_at?: string
          description?: string
          key?: string | null
          name: string
          parent_name?: string | null
          team_name: string
        }
        Update: {
          created_at?: string
          description?: string
          key?: string | null
          name?: string
          parent_name?: string | null
          team_name?: string
        }
        Relationships: [
          {
            foreignKeyName: "environments_parent_name_fkey"
            columns: ["parent_name"]
            isOneToOne: false
            referencedRelation: "environments"
            referencedColumns: ["name"]
          },
          {
            foreignKeyName: "environments_team_name_fkey"
            columns: ["team_name"]
            isOneToOne: false
            referencedRelation: "teams"
            referencedColumns: ["name"]
          },
        ]
      }
      profiles: {
        Row: {
          created_at: string
          id: string
          selected_team: string | null
        }
        Insert: {
          created_at?: string
          id: string
          selected_team?: string | null
        }
        Update: {
          created_at?: string
          id?: string
          selected_team?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "profiles_selected_team_fkey"
            columns: ["selected_team"]
            isOneToOne: false
            referencedRelation: "teams"
            referencedColumns: ["name"]
          },
        ]
      }
      teams: {
        Row: {
          created_at: string
          icon_url: string
          key: string | null
          name: string
        }
        Insert: {
          created_at?: string
          icon_url?: string
          key?: string | null
          name: string
        }
        Update: {
          created_at?: string
          icon_url?: string
          key?: string | null
          name?: string
        }
        Relationships: []
      }
      workflows: {
        Row: {
          created_at: string
          description: string
          environment_name: string
          name: string
          team_name: string
        }
        Insert: {
          created_at?: string
          description?: string
          environment_name: string
          name: string
          team_name: string
        }
        Update: {
          created_at?: string
          description?: string
          environment_name?: string
          name?: string
          team_name?: string
        }
        Relationships: [
          {
            foreignKeyName: "workflows_environment_team_fkey"
            columns: ["team_name", "environment_name"]
            isOneToOne: false
            referencedRelation: "environments"
            referencedColumns: ["team_name", "name"]
          },
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type PublicSchema = Database[Extract<keyof Database, "public">]

export type Tables<
  PublicTableNameOrOptions extends
    | keyof (PublicSchema["Tables"] & PublicSchema["Views"])
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
        Database[PublicTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
      Database[PublicTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : PublicTableNameOrOptions extends keyof (PublicSchema["Tables"] &
        PublicSchema["Views"])
    ? (PublicSchema["Tables"] &
        PublicSchema["Views"])[PublicTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  PublicEnumNameOrOptions extends
    | keyof PublicSchema["Enums"]
    | { schema: keyof Database },
  EnumName extends PublicEnumNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = PublicEnumNameOrOptions extends { schema: keyof Database }
  ? Database[PublicEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : PublicEnumNameOrOptions extends keyof PublicSchema["Enums"]
    ? PublicSchema["Enums"][PublicEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof PublicSchema["CompositeTypes"]
    | { schema: keyof Database },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof Database
  }
    ? keyof Database[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends { schema: keyof Database }
  ? Database[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof PublicSchema["CompositeTypes"]
    ? PublicSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never
