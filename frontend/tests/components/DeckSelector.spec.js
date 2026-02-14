import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import DeckSelector from '@/components/DeckSelector.vue'

describe('DeckSelector', () => {
  it('renders decks in dropdown', () => {
    const decks = [
      { id: 1, title: 'Spanish Basics' },
      { id: 2, title: 'Python Fundamentals' }
    ]
    
    const wrapper = mount(DeckSelector, {
      props: { decks, modelValue: '' }
    })
    
    expect(wrapper.text()).toContain('Spanish Basics')
    expect(wrapper.text()).toContain('Python Fundamentals')
  })

  it('emits update when deck selected', async () => {
    const wrapper = mount(DeckSelector, {
      props: { decks: [{ id: 1, title: 'Test' }], modelValue: '' }
    })
    
    await wrapper.find('select').setValue('1')
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual([1])
  })
})
